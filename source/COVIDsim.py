import sys
from random import randrange
from time import time, gmtime, strftime

from World import World
from Constants import Constants
from VaccineWarehouse import VaccineWarehouse
from Population import Population
from Config import VaccineApproach


class COVIDsim:
    """Container class to hold the algorithm and helper functions.

    Raises:
        ValueError: In case of wrong input we will return this error.
    """

    def __init__(self) -> None:
        """__init__
        """
        self.vaccinated_counter = 0
        self.vaccination_progress = []

        self.vaccines_amount_counter = 0
        self.vaccines_amount = []

        self.pfizer_amount_counter = 0
        self.pfizer_amount = []
        self.moderna_amount_counter = 0
        self.moderna_amount = []
        self.astrazeneca_amount_counter = 0
        self.astrazeneca_amount = []
        self.sputnik_amount_counter = 0
        self.sputnik_amount = []
        self.sinopharm_amount_counter = 0
        self.sinopharm_amount = []

    def progress_bar(self, count, total, bar_len=100):
        """Prints a progress bar to the console.

        Args:
            count (_type_): The current progress.
            total (_type_): The total goal.
            bar_len (int, optional): Length [character]. Defaults to 100.
        """
        filled_len = int(round(bar_len * count / float(total)))
        p_bar = '#' * filled_len + ' ' * (bar_len - filled_len)
        sys.stdout.write(f'[{p_bar}] {count+1}/{total}\r')
        sys.stdout.flush()

    def simulate(self, _w: World, vaccine_approach, capacity_increment: int = 0, discouraged_doctore: bool = True, print_bar: bool = False):
        """The main simulation algorithm

        Args:
            _w (World): The incoming "world" we will do the simulation on.
            vaccine_approach (_type_): Vaccine approach which determines how we
                                        would like to receive a new vaccine (random, etc).
            capacity_increment(int): If not default, then it will increase the districts capacity
                                        every day or in every offer_frequency day. Default 0.
            discouraged_doctore (bool, optional): True if the doctor get's discouraged from a refused vaccine.
                                                    If the doctor is discouraged it won't offer
                                                    the same vaccine again to anyone. Defaults to True.
            print_bar (bool, optional): If True it will print a progress bar to console. Defaults to False.

        Raises:
            ValueError: Returned in case of invalid vaccine_approach.
        """
        # reorder every districts every people list based on age and chronic disease
        _w.reorder_district_people_list(key=lambda k: (k.age, k.chronic_disease), reverse=True)
        is_age_between = False
        chronic_accepted = False

        for d in range(1, Constants.currentCfg.execution_time):
            self.vaccination_progress.append(self.vaccinated_counter)
            self.vaccines_amount.append(self.vaccines_amount_counter)
            self.pfizer_amount.append(self.pfizer_amount_counter)
            self.moderna_amount.append(self.moderna_amount_counter)
            self.astrazeneca_amount.append(self.astrazeneca_amount_counter)
            self.sputnik_amount.append(self.sputnik_amount_counter)
            self.sinopharm_amount.append(self.sinopharm_amount_counter)

            self.vaccines_amount_counter = 0
            self.pfizer_amount_counter = 0
            self.moderna_amount_counter = 0
            self.astrazeneca_amount_counter = 0
            self.sputnik_amount_counter = 0
            self.sinopharm_amount_counter = 0

            if print_bar:
                self.progress_bar(d, Constants.currentCfg.execution_time)

            for district in _w.district_list:
                selected_vaccine = None
                # decrement every person's wait counter. Which was incremented on a refusal.
                district.decrement_wait()
                # reset the vaccine probability. Important if the doctor is discouraged.
                district.reset_vaccine_prob()
                # reset the district capacity.
                district.capacity = Constants.currentCfg.district_capacity

                # district person id counter
                dp_id = 0

                self.vaccines_amount_counter += district.get_vaccines_amount()
                self.pfizer_amount_counter += district.get_spec_vacc_amount("pfizer")
                self.moderna_amount_counter += district.get_spec_vacc_amount("moderna")
                self.astrazeneca_amount_counter += district.get_spec_vacc_amount("astrazeneca")
                self.sputnik_amount_counter += district.get_spec_vacc_amount("sputnik")
                self.sinopharm_amount_counter += district.get_spec_vacc_amount("sinopharm")

                while dp_id < len(district.people_list) and district.capacity > 0:
                    if vaccine_approach == VaccineApproach.RANDOM_VACCINE:
                        selected_vaccine = district.get_random_vaccine()
                        if selected_vaccine is None:
                            # if we can not get a random vaccine that means
                            # we don't have any remaining vaccines in the district's warehouse.
                            break
                    elif vaccine_approach == VaccineApproach.PREFERENCE_BASED_VACCINE:
                        selected_vaccine = district.get_vaccine_for_people(dp_id)
                        if selected_vaccine is None:
                            dp_id += 1
                            # if we can not get a vaccine for a specific people then we should move on to the next one.
                            continue
                    else:
                        raise ValueError("Invalid parameter: \n" + str(vaccine_approach))

                    # check if the person's preference list matches the selected_vaccine
                    for dp_pref in district.people_list[dp_id].preference_list:
                        if district.people_list[dp_id].last_rejected != 0 or \
                                district.people_list[dp_id].accepted or \
                                district.capacity == 0:
                            break

                        if dp_pref[0] == selected_vaccine.name:
                            # the selected vaccine is in the preference list.

                            is_age_between = district.people_list[dp_id].age >= selected_vaccine.min_suggested_age and \
                                district.people_list[dp_id].age <= selected_vaccine.max_suggested_age

                            chronic_accepted = (not district.people_list[dp_id].chronic_disease) or \
                                (district.people_list[dp_id].chronic_disease and selected_vaccine.suggested_to_chronic)

                            if chronic_accepted and is_age_between:
                                district.people_list[dp_id].offered_counter += 1
                                selected_vaccine.offered_counter += 1
                                district.capacity -= 1

                                # random decision based on the preference
                                if randrange(100) < dp_pref[1]:
                                    district.people_list[dp_id].accepted = True
                                    district.people_list[dp_id].selected_vaccine = selected_vaccine.name
                                    selected_vaccine.vaccine_amount -= 1
                                    selected_vaccine.vaccine_prob -= 1
                                    self.vaccinated_counter += 1
                                else:
                                    district.people_list[dp_id].accepted = False
                                    for dp_rej in range(len(district.people_list[dp_id].rejected_list)):
                                        rej_tuple = district.people_list[dp_id].rejected_list[dp_rej]
                                        if rej_tuple[0] == selected_vaccine.name:
                                            temp_list = list(rej_tuple)
                                            temp_list[1] += 1
                                            temp_tuple = tuple(temp_list)
                                            district.people_list[dp_id].rejected_list[dp_rej] = temp_tuple
                                    district.people_list[dp_id].last_rejected = Constants.currentCfg.offer_frequency
                                    selected_vaccine.refused_counter += 1
                                    if discouraged_doctore:
                                        selected_vaccine.vaccine_prob -= 1
                            break

                    dp_id += 1

            if d % Constants.currentCfg.offer_frequency == 0:
                _w.warehouse.increment_shipment(Constants.currentCfg.offer_frequency)
                _w.redistribute()
                Constants.currentCfg.district_capacity += capacity_increment
            # put this to the if above if we would only like to increase in every offer_frequency day
            # or put it below if we would like to increase it every day
            #Constants.currentCfg.district_capacity += capacity_increment


if __name__ == "__main__":
    # Start time measurement.
    start_time = time()

    # sets the default config. Change it to test a different scenario
    Constants.currentCfg = Constants.execConfig

    warehouse = VaccineWarehouse()

    population = Population()
    # generate random population
    # population.generate_random_population(Constants.currentCfg.population_size, warehouse.vaccine_list)
    # generate representative population
    population.generate_representative_population(Constants.currentCfg.population_size, warehouse.vaccine_list)

    world = World(warehouse, population)

    # simulate based on random vaccine distribution
    covid = COVIDsim()
    # covid.simulate(world, VaccineApproach.RANDOM_VACCINE, True, True)
    # simulate based on preference
    covid.simulate(world, VaccineApproach.PREFERENCE_BASED_VACCINE, 0, True, True)

    # end time measurement
    elapsed_time = time() - start_time
    print('Execution time:', strftime("%H:%M:%S", gmtime(elapsed_time)), "\n")
