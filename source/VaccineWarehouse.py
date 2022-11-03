from ast import Num
from operator import itemgetter
from random import choices, randrange, sample, shuffle
import random
from unittest import skip
from numpy import datetime_as_string
import numpy as np
from openpyxl import load_workbook
import pandas as pd
from time import time, gmtime, strftime
from tabulate import tabulate
from datetime import datetime, timedelta
from copy import deepcopy

from Constants import Constants
from DataHandler import DataHandler
from Vaccine import Vaccine


class VaccineWarehouse:
    def __init__(self):
        self.last_date = datetime.strptime(Constants.currentCfg.shipment_start_date, "%Y-%m-%d")
        self.vaccine_list = []
        self.vaccine_logbook = pd.DataFrame()
        self.dh = DataHandler()
        self.import_shipments(Constants.shipment_file)
        self.import_parameters(Constants.parameter_file)

    def __recalculate_vaccine_ratio(self):
        temp = np.array([x.last_increment for x in self.vaccine_list])
        temp = temp / temp.sum()

        for i in range(len(self.vaccine_list)):
            self.vaccine_list[i].last_shipment_percentage = temp[i]*100

    def __vaccine_between(self, date1, date2, vaccine_name) -> int:
        idx1 = self.vaccine_logbook.index[pd.to_datetime(self.vaccine_logbook["date"]) == date1].tolist()[0]
        idx2 = self.vaccine_logbook.index[pd.to_datetime(self.vaccine_logbook["date"]) == date2].tolist()[0]

        return self.vaccine_logbook[vaccine_name].values[idx2] - self.vaccine_logbook[vaccine_name].values[idx1]

    def import_shipments(self, data_file: str):
        self.vaccine_logbook = self.dh.from_xlsx(data_file)

    def import_parameters(self, data_file: str):
        vaccineParameters = self.dh.from_xlsx(data_file)

        idx = self.vaccine_logbook.index[pd.to_datetime(self.vaccine_logbook["date"]) == self.last_date].tolist()[0]

        for x in vaccineParameters.index:
            first_vaccine_ammount = self.vaccine_logbook[vaccineParameters["name"][x]].values[idx]
            self.vaccine_list.append(Vaccine(name=vaccineParameters["name"][x],
                                             vaccine_amount=int(first_vaccine_ammount / Constants.currentCfg.vaccine_divider),
                                             vaccine_prob=int(first_vaccine_ammount / Constants.currentCfg.vaccine_divider),
                                             last_increment=first_vaccine_ammount,
                                             last_shipment_percentage=0,
                                             suggested_to_chronic=(vaccineParameters["suggested_to_chronic"][x] == "yes"),
                                             min_suggested_age=vaccineParameters["min_suggested_age"][x],
                                             max_suggested_age=vaccineParameters["max_suggested_age"][x]))

        self.__recalculate_vaccine_ratio()

    def increment_shipment(self, number_of_days: int):
        currentDate = self.last_date + timedelta(days=number_of_days)

        for x in self.vaccine_list:
            x.last_increment = self.__vaccine_between(self.last_date, currentDate, x.name)
            x.vaccine_amount += int(x.last_increment / Constants.currentCfg.vaccine_divider)
            x.vaccine_prob = x.vaccine_amount

        self.last_date = currentDate
        self.__recalculate_vaccine_ratio()

    def get_vaccine_portion(self, vaccine_ratio: int) -> list:
        portions = []
        vaccin_multiplier = ((100.0-Constants.currentCfg.vaccine_reserve_ratio)/100.0)/vaccine_ratio
        vaccin_list_decrement = [0]*len(self.vaccine_list)

        for i in range(vaccine_ratio):
            portion = []
            for j in range(len(self.vaccine_list)):
                temp = deepcopy(self.vaccine_list[j])
                temp.vaccine_amount = int(temp.vaccine_amount * vaccin_multiplier)
                temp.vaccine_prob = temp.vaccine_amount
                vaccin_list_decrement[j] += temp.vaccine_amount
                portion.append(temp)
            portions.append(portion)

        for j in range(len(self.vaccine_list)):
            self.vaccine_list[j].vaccine_amount -= vaccin_list_decrement[j]
            self.vaccine_list[j].vaccine_prob -= vaccin_list_decrement[j]

        return portions
