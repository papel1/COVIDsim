from dataclasses import dataclass


@dataclass
class People:
    """
    Represents a person.

    Attributes:
        id                  A persons unique identifier.
        age                 The persons age.
        district_id         The district the person inhabits.
        preference_list     The persons vaccine preference list.
        chronic_disease     A logic value which will be true if the person has a chronic disease.
        last_rejected       The number of days remaining before we can offer a new vaccine to the person.
        accepted            A logic value which will be true if the person has accepted a vaccine.
        selected_vaccine    The name of the selected vaccine.
        offered_counter     A counter which will be incremented with every offer.
    """

    id: int
    age: int
    district_id: int
    preference_list: list
    chronic_disease: bool
    last_rejected: int = 0
    accepted: bool = False
    selected_vaccine: str = ""
    offered_counter: int = 0
