from random import randrange, sample

from People import People
from Constants import Constants


class Population:
    """
    Class that represents the whole population in our simulation.
    """

    def __init__(self):
        self.people_list = []

    def import_population(self, population_path):
        """Import a population from file.

        Args:
            population_path (_type_): Path to the file we would like to import
        """
        # TODO: read from xls
        pass

    def generate_representative_population(self, num_of_people, vaccine_list: list):
        """
        Generate a representative population.
        Based on age.
        Chronic disease distribution compared to age.
        Proper (not random) preference list.

        Args:
            num_of_people (_type_): The number of people we would like to generate.
        """
        # TODO:
        # based on age anc chronic disease while considering the age to chronic disease ratio.
        # with the preference list not as a random one but one that mirrorst the real world.
        pass

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
                                  Constants.currentCfg.population_max_age),
                    district_id=-1,
                    preference_list=sorted([(vac.name, randrange(1, 100))
                                            for vac in pref_vacc],
                                           key=lambda x: x[1], reverse=True),
                    chronic_disease=randrange(100) < Constants.currentCfg.chronic_disease_ratio
                ))
