from operator import itemgetter
from random import choices, randrange, sample, shuffle
from numpy import datetime_as_string
from openpyxl import load_workbook
import pandas as pd
from time import time, gmtime, strftime
from tabulate import tabulate

from World import World
from Constants import Constants
from VaccineWarehouse import VaccineWarehouse
from Population import Population


def reorder_district_people_list(_w: World):
    for d in _w.district_list:
        d.people_list.sort(key=lambda k: (k.age, k.chronic_disease), reverse=True)


def simulate(_w: World):
    reorder_district_people_list(_w)
    is_age_between = False
    chronic_accepted = False

    for d in range(1, Constants.currentCfg.execution_time):
        # TODO: use district_capacity
        for district in _w.district_list:
            district.decrement_wait()
            district.reset_vaccine_prob()
            dp_id = 0

            while dp_id < len(district.people_list):
                # TODO: maybe just the vaccine id will this edit the list element?
                random_vaccine = district.get_random_vaccine()

                if random_vaccine is None:
                    break

                for dp_pref in district.people_list[dp_id].preference_list:
                    if district.people_list[dp_id].last_rejected != 0 or district.people_list[dp_id].accepted:
                        break

                    if dp_pref[0] == random_vaccine.name:
                        is_age_between = district.people_list[dp_id].age >= random_vaccine.min_suggested_age and \
                            district.people_list[dp_id].age <= random_vaccine.max_suggested_age

                        chronic_accepted = (not district.people_list[dp_id].chronic_disease) or \
                            (district.people_list[dp_id].chronic_disease and random_vaccine.suggested_to_chronic)

                        if chronic_accepted and is_age_between:
                            district.people_list[dp_id].offered_counter += 1

                            if randrange(100) < dp_pref[1]:
                                district.people_list[dp_id].accepted = True
                                district.people_list[dp_id].selected_vaccine = random_vaccine.name
                                random_vaccine.vaccine_amount -= 1
                                random_vaccine.vaccine_prob -= 1
                            else:
                                district.people_list[dp_id].accepted = False
                                district.people_list[dp_id].last_rejected = Constants.currentCfg.offer_frequency
                                random_vaccine.vaccine_prob -= 1
                        break

                dp_id += 1

        if d % Constants.currentCfg.offer_frequency == 0:
            _w.warehouse.increment_shipment(Constants.currentCfg.offer_frequency)
            _w.redistribute()

if __name__ == "__main__":
    start_time = time()

    Constants.currentCfg = Constants.testCfg

    warehouse = VaccineWarehouse()

    population = Population()
    population.generate_random_population(Constants.currentCfg.population_size, warehouse.vaccine_list)  # TODO: repr

    world = World(warehouse, population)

    simulate(world)

    elapsed_time = time() - start_time
    print('Execution time:', strftime("%H:%M:%S", gmtime(elapsed_time)), "\n")
