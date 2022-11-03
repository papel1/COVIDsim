from ast import Num
from operator import itemgetter
from random import choices, randrange, sample, shuffle
import random
from unittest import skip
from numpy import datetime_as_string
import numpy
from openpyxl import load_workbook
import pandas as pd
from time import time, gmtime, strftime
from tabulate import tabulate

from Constants import Constants
from VaccineWarehouse import VaccineWarehouse
from District import District
from Population import Population


class World:
    def __init__(self, _w: VaccineWarehouse, _p: Population):
        assert Constants.currentCfg is not None, "Please select a default config!"

        self.warehouse = _w
        self.population = _p
        self.district_list = []

        self.assign_people_to_districts()

    def __splitter(self, p_list, size):
        return list(p_list[i::size] for i in range(size))

    def assign_people_to_districts(self):
        split_people_list = self.__splitter(self.population.people_list, Constants.currentCfg.district_size)
        portions = self.warehouse.get_vaccine_portion(Constants.currentCfg.district_size)

        for x in range(Constants.currentCfg.district_size):
            temp_district = District(
                id=x,
                vaccine_list=portions[x],
                people_list=split_people_list[x]
            )

            for d in temp_district.people_list:
                d.district_id = x

            self.district_list.append(temp_district)

    def redistribute(self):
        portions = self.warehouse.get_vaccine_portion(Constants.currentCfg.district_size)

        for i in range(len(self.district_list)):
            for v in self.district_list[i].vaccine_list:
                for t in portions[i]:
                    if t.name == v.name:
                        v.vaccine_amount += t.vaccine_amount
                        v.vaccine_prob = v.vaccine_amount
