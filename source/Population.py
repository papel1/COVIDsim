from random import randrange, sample

import pandas as pd

from People import People
from Constants import Constants
from DataHandler import DataHandler


class Population:
    """
    Class that represents the whole population in our simulation.
    """

    def __init__(self):
        self.people_list = []
        self.dh = DataHandler(Constants.data_folder, Constants.output_folder)
        self.representative_population = pd.DataFrame()
        self.import_population(Constants.population_file)

    def import_population(self, data_file: str):
        """Import a population from file.

        Args:
            data_file (str): Path to the file we would like to import.
        """
        self.representative_population = self.dh.from_xlsx(data_file)

    def generate_representative_population(self, num_of_people, vaccine_list: list):
        """
        Generate a representative population.
        Based on age.
        Chronic disease distribution compared to age.

        Args:
            num_of_people (_type_): The number of people we would like to generate.
            vaccine_list (list): The list of vaccines the population can choose from.
        """

        assert num_of_people > 0, "The number of people should be greater than 0!"
        self.people_list = []

        for x in self.representative_population.index:
            for y in range(int(self.representative_population["ratio"].values[x]*num_of_people)):
                pref_num = randrange(0, len(vaccine_list)+1)
                pref_vacc = sample(vaccine_list, pref_num)

                self.people_list.append(
                    People(
                        id=y + 1,
                        age=randrange(self.representative_population["min_age"].values[x],
                                      self.representative_population["max_age"].values[x]+1),
                        district_id=-1,
                        preference_list=sorted([(vac.name, randrange(1, 101))
                                                for vac in pref_vacc],
                                               key=lambda x: x[1], reverse=True),
                        chronic_disease=randrange(100) < int(self.representative_population["chronic_disease_ratio"].values[x]*100),
                        rejected_list=[(vac.name, int(0)) for vac in vaccine_list]
                    ))

    def generate_random_population(self, num_of_people: int, vaccine_list: list):
        """Generates a random population.

        Args:
            num_of_people (int): The number of people we would like to generate.
            vaccine_list (list): The list of vaccines the population can choose from.
        """
        assert num_of_people > 0, "The number of people should be greater than 0!"
        self.people_list = []

        for x in range(num_of_people):
            pref_num = randrange(0, len(vaccine_list)+1)
            pref_vacc = sample(vaccine_list, pref_num)

            self.people_list.append(
                People(
                    id=x + 1,
                    age=randrange(Constants.currentCfg.population_min_age,
                                  Constants.currentCfg.population_max_age+1),
                    district_id=-1,
                    preference_list=sorted([(vac.name, randrange(1, 101))
                                            for vac in pref_vacc],
                                           key=lambda x: x[1], reverse=True),
                    chronic_disease=randrange(100) < Constants.currentCfg.chronic_disease_ratio,
                    rejected_list=[(vac.name, int(0)) for vac in vaccine_list]
                ))
