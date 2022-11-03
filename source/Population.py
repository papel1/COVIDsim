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

from People import People
from Constants import Constants


class Population:
    def __init__(self):
        self.people_list = []

    def import_population(self, population_path):
        # TODO: read from xls
        pass

    def generate_representative_population(self, num_of_people):
        # TODO:
        # based on age anc chronic disease while considering the age to chronic disease ratio
        # with the preference list not as a random one but one that mirrorst the real world
        pass

    def generate_random_population(self, num_of_people: int, vaccine_list: list):
        assert num_of_people > 0, "The number of people should be greater than 0!"
        self.people_list = []

        for x in range(num_of_people):
            pref_num = randrange(0, len(vaccine_list)+1)
            pref_vacc = sample(vaccine_list, pref_num)

            self.people_list.append(
                People(
                    id=x + 1,
                    age=randrange(Constants.currentCfg.population_min_age,
                                  Constants.currentCfg.population_max_age),
                    district_id=-1,
                    preference_list=sorted([(vac.name, randrange(1, 100)) for vac in pref_vacc], key=lambda x: x[1], reverse=True),
                    chronic_disease=random.randrange(100) < Constants.currentCfg.chronic_disease_ratio
                ))
