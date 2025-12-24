from geopy import Location
from geopy.geocoders import Nominatim

from application.enums.services.country import Country


async def get_location(country: Country, city: str, street: str, house_number: str, postal_code: str) -> Location:
    geolocator = Nominatim(user_agent="car-service")
    address = f"{street} {house_number} {postal_code} {city} {country.value.title()}"
    location: Location = geolocator.geocode(address)
    return location
