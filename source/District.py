from dataclasses import dataclass
from random import choices

from Vaccine import Vaccine


@dataclass
class District:
    """_summary_

    Attributes:
        id              The districts unique identifier.
        capacity        The maximum ammount of vaccine a district can offer in a given day.
        vaccine_list    The districts own vaccine warehouse.
        people_list     The list of people in this district.
    """

    id: int
    capacity: int
    vaccine_list: list
    people_list: list

    def get_random_vaccine(self) -> Vaccine:
        """Returns a random vaccine based on the corresponding vaccine_prob.

        Returns:
            Vaccine: The result vaccine.
        """
        result = None
        temp = [x for x in self.vaccine_list
                if x.vaccine_amount > 0 and x.vaccine_prob > 0]

        if len(temp) > 0:
            result = choices(population=temp,
                             weights=[x.vaccine_prob for x in self.vaccine_list
                                      if x.vaccine_amount > 0 and x.vaccine_prob > 0],
                             k=1)[0]

        return result

    def get_vaccine_for_people(self, dp_id: int) -> Vaccine:
        """Returns a suggested vaccine based on the preference_list.

        Args:
            dp_id (int): The person's id which we should give the vaccine.

        Returns:
            Vaccine: The best vaccine we could provide.
        """
        result = None

        for pref in self.people_list[dp_id].preference_list:
            if result is not None:
                break
            for vac in self.vaccine_list:
                if vac.vaccine_amount > 0 and pref[0] == vac.name:
                    result = vac
                    break

        return result

    def decrement_wait(self):
        """ Decrements the last_rejected counter for every related person.
        """
        for p in self.people_list:
            if p.last_rejected > 0:
                p.last_rejected -= 1

    def reset_vaccine_prob(self):
        """
        Resets the vaccine's probability to the vaccine_amount.
        This is needed if we had refused vaccines.
        """
        for v in self.vaccine_list:
            v.vaccine_prob = v.vaccine_amount
