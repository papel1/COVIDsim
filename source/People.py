from dataclasses import dataclass


@dataclass
class People:
    """
    Represents a person.
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
