from enum import Enum

class BodyType(str, Enum):
    # Passenger cars
    HATCHBACK = "Hatchback"
    SEDAN = "Sedan"
    ESTATE = "Estate"
    COUPE = "Coupe"
    COUPE_SUV = "Coupe SUV"
    FASTBACK = "Fastback"
    CONVERTIBLE = "Convertible"
    ROADSTER = "Roadster"

    # SUVs & Crossovers
    SUV = "SUV"
    CROSSOVER = "Crossover"
    OFF_ROAD = "Off-road"

    # Multi-purpose
    MPV = "MPV"
    MINIVAN = "Minivan"
    MICROVAN = "Microvan"

    # Commercial - light
    VAN = "Van"
    MINIBUS = "Minibus"
    PICKUP = "Pickup"

    # Commercial - heavy
    TRUCK = "Truck"
    SEMI_TRUCK = "Semi-truck"
    TIPPER = "Tipper"
    BOX_TRUCK = "Box Truck"
    REFRIGERATED_TRUCK = "Refrigerated Truck"
    TANKER = "Tanker"
    FLATBED = "Flatbed"

    # Buses
    BUS = "Bus"
    COACH = "Coach"
    SCHOOL_BUS = "School Bus"
    ARTICULATED_BUS = "Articulated Bus"

    # Special / Other
    AMBULANCE = "Ambulance"
    FIRE_TRUCK = "Fire Truck"
    TRACTOR = "Tractor"
    FORKLIFT = "Forklift"
    OTHER = "Other"