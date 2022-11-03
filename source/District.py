from dataclasses import dataclass

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

from Vaccine import Vaccine


@dataclass
class District:
    id: int
    vaccine_list: list
    people_list: list

    def get_random_vaccine(self) -> Vaccine:
        result = None
        temp = [x for x in self.vaccine_list
                if x.vaccine_amount > 0 and x.vaccine_prob > 0]

        if len(temp) > 0:
            result = random.choices(population=temp,
                                    weights=[x.vaccine_prob for x in self.vaccine_list
                                             if x.vaccine_amount > 0 and x.vaccine_prob > 0],
                                    k=1)[0]

        return result

    def decrement_wait(self):
        for p in self.people_list:
            if p.last_rejected > 0:
                p.last_rejected -= 1

    def reset_vaccine_prob(self):
        for v in self.vaccine_list:
            v.vaccine_prob = v.vaccine_amount
