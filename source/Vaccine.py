from dataclasses import dataclass


@dataclass
class Vaccine:
    """
    Represents a vaccine.

    Attributes:
        name                    The name of the vaccine.
        vaccine_amount          The ammount of vaccines we have.
        last_increment          The last shippment arrival.
        last_shipment_perc      The percentage of the last shipment of this specific vaccine.
        suggested_to_chronic    Boolean which determines if the vaccine is suggested to a person with chronic disease.

        min_suggested_age       Minimum required age for the vaccine.
        max_suggested_age       Maximum allowed age for the vaccine
    """

    name: str
    vaccine_amount: int
    vaccine_prob: int
    last_increment: int
    last_shipment_percentage: float

    suggested_to_chronic: bool

    min_suggested_age: int = 12
    max_suggested_age: int = 113
