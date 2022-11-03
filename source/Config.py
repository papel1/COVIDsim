from dataclasses import dataclass


@dataclass
class Config:
    """
    Contains every basic configuration info with which we can start the algorithm.

    Attributes:
        execution_time          Number of days the olgorithm should simulate.

        population_size         The number of people the algorithm should work on.
        population_min_age      The minimum age for a generated person.
        population_max_age      The maximum age for a generated person.
        chronic_disease_ratio   The ratio whic determines how many people has a chronic disease. [percentage]

        shipment_start_date     The date when we received the first vaccine. should match a date from data.
        shipment_frequency      The frequency which determines how often we will receive a new vaccine shipment. [day]

        district_size           The number of district we should partition to.
        district_capacity       The number of offer a district can do in any given day.
        vaccine_reserve_ratio   The ammount of vaccine we should not distribute and keep as backup.

        offer_frequency         The frequency with which we will offer a vaccine to a person who has refused a previous offer. [day]
        vaccine_divider         The number which we should divide our vacines with in order to mimic a more realistic scenario.
    """

    execution_time: int

    population_size: int
    population_min_age: int
    population_max_age: int
    chronic_disease_ratio: int

    shipment_start_date: str
    shipment_frequency: int

    district_size: int
    district_capacity: int
    vaccine_reserve_ratio: float

    offer_frequency: int

    vaccine_divider: int
