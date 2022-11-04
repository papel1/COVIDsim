from Constants import Constants
from VaccineWarehouse import VaccineWarehouse
from District import District
from Population import Population


class World:
    """
    Represents the whole world in our experiment.
    """

    def __init__(self, _w: VaccineWarehouse, _p: Population):
        """__init__

        Args:
            _w (VaccineWarehouse): Input VaccineWarehouse to our simulation.
            _p (Population): Input Population to our simulation.
        """
        assert Constants.currentCfg is not None, "Please select a default config!"

        self.warehouse = _w
        self.population = _p
        self.district_list = []

        self.__assign_people_to_districts()

    def __splitter(self, p_list, size):
        """Splits a list to n equal sized smaller list.

        Args:
            p_list (_type_): The list we would like to split.
            size (_type_): The number of parts we would like to split the original list.

        Returns:
            _type_: List of lists. Containing the split lists.
        """
        return list(p_list[i::size] for i in range(size))

    def __assign_people_to_districts(self):
        """
        Assings the population to the districts randomly.
        """
        split_people_list = self.__splitter(self.population.people_list, Constants.currentCfg.district_size)
        portions = self.warehouse.get_vaccine_portion(Constants.currentCfg.district_size)

        for x in range(Constants.currentCfg.district_size):
            temp_district = District(
                id=x,
                capacity=Constants.currentCfg.district_capacity,
                vaccine_list=portions[x],
                people_list=split_people_list[x]
            )

            for d in temp_district.people_list:
                d.district_id = x

            self.district_list.append(temp_district)

    def redistribute(self):
        """
        With the help of this method we can redistribute the incoming vaccine shipment among the districts.
        """
        portions = self.warehouse.get_vaccine_portion(Constants.currentCfg.district_size)

        for i in range(len(self.district_list)):
            for v in self.district_list[i].vaccine_list:
                for t in portions[i]:
                    if t.name == v.name:
                        v.vaccine_amount += t.vaccine_amount
                        v.vaccine_prob = v.vaccine_amount

    def reorder_district_people_list(self, key, reverse):
        """Reorders every districts population based on the inputs.

        Args:
            key (_type_): Lambda function which serves as the key for the sort function.
            reverse (_type_): Reverse flag.
        """
        for d in self.district_list:
            d.people_list.sort(key=key, reverse=reverse)
