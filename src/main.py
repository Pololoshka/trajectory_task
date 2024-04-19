import os

from src.models import Vehicle
from src.vehicle_manager.manager import VehicleManager

URL = os.environ.get("VEHICELS_API_URL", "https://test.tspb.su/test-task")


def main() -> None:
    manager = VehicleManager(url=URL)
    print(manager.get_vehicles())
    """
    [Vehicle(name='Toyota', model='Camry', year=2021, color='red', price=21000,
    latitude=55.753332, longitude=37.621676, id=1), ...]
    """

    print(manager.filter_vehicles(params={"name": "Toyota"}))
    """
    [Vehicle(name='Toyota', model='Camry', year=2021, color='red', price=21000,
    latitude=55.753332, longitude=37.621676, id=1)]
    """

    print(manager.get_vehicle(vehicle_id=1))
    """
    Vehicle(name='Toyota', model='Camry', year=2021, color='red', price=21000,
    latitude=55.753332, longitude=37.621676, id=1)
    """

    print(
        manager.add_vehicle(
            vehicle=Vehicle(
                name="Toyota",
                model="Camry",
                year=2021,
                color="red",
                price=21000,
                latitude=55.753215,
                longitude=37.620393,
            )
        )
    )
    """
    Vehicle(name='Toyota', model='Camry', year=2021, color='red', price=21000,
    latitude=55.753215, longitude=37.620393, id=21)
    """

    print(
        manager.update_vehicle(
            vehicle=Vehicle(
                id=1,
                name="Toyota",
                model="Camry",
                year=2021,
                color="red",
                price=21000,
                latitude=55.753215,
                longitude=37.620393,
            )
        )
    )
    """
    Vehicle(name='Toyota', model='Camry', year=2021, color='red', price=21000,
    latitude=55.753215, longitude=37.620393, id=1)
    """

    print(manager.delete_vehicle(vehicle_id=1))  # type: ignore
    """
    None
    """
    print(manager.get_distance(id1=1, id2=2))
    """
    638005.0864183326
    """
    print(manager.get_nearest_vehicle(vehicle_id=1))
    """
    Vehicle(name='Tesla', model='Model 3', year=2019, color='white', price=60000,
    latitude=59.829604, longitude=30.374407, id=18)
    """


if __name__ == "__main__":
    main()
