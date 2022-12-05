from Config import Config


class Constants:
    """
    Contains a couple of basic pre determined configuration with constants.
    """

    testCfg = Config(
        execution_time=50,
        population_size=10000,
        population_min_age=16,
        population_max_age=113,
        chronic_disease_ratio=25,
        shipment_start_date="2021-02-16",
        shipment_frequency=7,
        district_size=5,
        district_capacity=20,
        vaccine_reserve_ratio=20.0,
        offer_frequency=7,
        vaccine_divider=1000,
        strong_desire_for_vacc=0  # original solution is with 0
    )

    execConfig = Config(
        execution_time=200,
        population_size=100000,
        population_min_age=16,
        population_max_age=113,
        chronic_disease_ratio=25,
        shipment_start_date="2021-01-01",
        shipment_frequency=7,
        district_size=44,
        district_capacity=40,
        vaccine_reserve_ratio=20.0,
        offer_frequency=7,
        vaccine_divider=100,
        strong_desire_for_vacc=51
    )

    realConfig = Config(
        execution_time=365,
        population_size=10000000,
        population_min_age=16,
        population_max_age=113,
        chronic_disease_ratio=25,
        shipment_start_date="2021-02-16",
        shipment_frequency=7,
        district_size=4473,
        district_capacity=100,
        vaccine_reserve_ratio=20.0,
        offer_frequency=7,
        vaccine_divider=1,
        strong_desire_for_vacc=51
    )

    currentCfg = None

    data_folder = "./data/"
    output_folder = "./output/"
    parameter_file = "vacc_parameters"
    shipment_file = "vacc_shipment"
    population_file = "population_age_groups"
    real_vacc_file = "real_vaccination"
