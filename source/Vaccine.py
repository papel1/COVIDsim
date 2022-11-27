from dataclasses import dataclass


@dataclass
class Vaccine:
    """
    Represents a vaccine.

    Attributes:
        name                    The name of the vaccine.
        vaccine_amount          The ammount of vaccines we have.
        vaccine_prob            The "probability" that we can choose this vaccine.
                                    The initial value is same as the vaccine_amount.
                                    During execution if the discuraged flag is turned on during simulation the doctor will not
                                    offer a vaccine if it was already refused.
                                    We can not remove the vaccine from the vaccine_amount since the amount wouldn't change.
                                    In that case, we couldn't throw the vaccine away.
                                    But we can introduce this variable to note if a vaccine "type" was refused.
        last_increment          The last shippment arrival.
        last_shipment_perc      The percentage of the last shipment of this specific vaccine.

        suggested_to_chronic    Boolean which determines if the vaccine is suggested to a person with chronic disease.

        min_suggested_age       Minimum required age for the vaccine.
        max_suggested_age       Maximum allowed age for the vaccine.

        refused_counter         The number of times the vaccine got refused.
        offered_counter         The number of times the vaccine had been offered.
    """

    name: str
    vaccine_amount: int
    vaccine_prob: int
    last_increment: int
    last_shipment_perc: float

    suggested_to_chronic: bool

    min_suggested_age: int = 12
    max_suggested_age: int = 113

    refused_counter: int = 0
    offered_counter: int = 0
