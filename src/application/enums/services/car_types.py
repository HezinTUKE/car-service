from enum import Enum


class CarType(str, Enum):
    # Passenger cars
    SEDAN = "SEDAN"
    HATCHBACK = "HATCHBACK"
    COUPE = "COUPE"
    CONVERTIBLE = "CONVERTIBLE"
    WAGON = "WAGON"
    LIFTBACK = "LIFTBACK"

    # Performance & luxury
    SPORTS = "SPORTS"
    SUPER_CAR = "SUPER_CAR"
    LUXURY = "LUXURY"
    CLASSIC = "CLASSIC"

    # SUVs & off-road
    SUV = "SUV"
    CROSSOVER = "CROSSOVER"
    OFF_ROAD = "OFF_ROAD"

    # Commercial & utility
    PICKUP = "PICKUP"
    TRUCK = "TRUCK"
    VAN = "VAN"
    MINIVAN = "MINIVAN"
    BUS = "BUS"
    BOX_TRUCK = "BOX_TRUCK"

    # Powertrain types
    ELECTRIC = "ELECTRIC"
    HYBRID = "HYBRID"
    PLUG_IN_HYBRID = "PLUG_IN_HYBRID"
    HYDROGEN = "HYDROGEN"

    # Special purpose
    TAXI = "TAXI"
    POLICE = "POLICE"
    AMBULANCE = "AMBULANCE"
    FIRE_TRUCK = "FIRE_TRUCK"
    MILITARY = "MILITARY"

    # Two & three wheelers (optional, remove if not needed)
    MOTORCYCLE = "MOTORCYCLE"
    SCOOTER = "SCOOTER"

    ALL = "ALL"
