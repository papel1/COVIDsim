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


class DataHandler:
    def __init__(self):
        pass

    def to_xlsx(self, data_container, name: str):
        df = pd.DataFrame(data=data_container)
        df.to_excel(Constants.data_folder + f"{name}.xlsx")

    def from_xlsx(self, name: str) -> pd.DataFrame:
        return pd.read_excel(Constants.data_folder + name)
