import math
from dataclasses import asdict, fields
from typing import Any

from src.models import Vehicle
from src.vehicle_manager.api import API


class VehicleManager:
    def __init__(self, url: str, timeout: int = 5) -> None:
        self.api = API(url=url, timeout=timeout)

    def get_vehicles(self) -> list[Vehicle]:
        response = self.api.get_list()
        return [Vehicle.parse(data=value) for value in response]

    def filter_vehicles(self, params: dict[str, Any]) -> list[Vehicle]:
        fields_vehicle = {field.name: field.type for field in fields(Vehicle)}

        if error_attrs := set(params).difference(set(fields_vehicle)):
            raise AttributeError(f"'Vehicle' object has no attributes: {error_attrs}")
        for key, value in params.items():
            if not isinstance(value, fields_vehicle[key]):
                raise TypeError(
                    f"'Vehicle.{key}' has type {fields_vehicle[key]} received {type(value)}"
                )

        result = []
        for vehicle in self.get_vehicles():
            for key, value in params.items():
                if getattr(vehicle, key) != value:
                    break
            else:
                result.append(vehicle)

        return result

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        response = self.api.get(vehicle_id=vehicle_id)
        return Vehicle.parse(data=response)

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        data = asdict(vehicle)
        data.pop("id", None)
        response = self.api.create(vehicle=data)
        return Vehicle.parse(data=response)

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        if not vehicle.id:
            raise ValueError("'Vehicle' object attribute 'id' must be not None")

        response = self.api.update(vehicle_id=vehicle.id, vehicle=asdict(vehicle))
        return Vehicle.parse(data=response)

    def delete_vehicle(self, vehicle_id: int) -> None:
        self.api.delete(vehicle_id=vehicle_id)

    def get_distance(self, id1: int, id2: int) -> float:
        vehicle1 = self.get_vehicle(vehicle_id=id1)
        vehicle2 = self.get_vehicle(vehicle_id=id2)
        return self._calculate_distance(vehicle1, vehicle2)

    def get_nearest_vehicle(self, vehicle_id: int) -> Vehicle | None:
        cur_vehicle = self.get_vehicle(vehicle_id=vehicle_id)
        vehicles = self.get_vehicles()
        if len(vehicles) == 1:
            return None
        nearest_vehicle = min(
            (vehicle for vehicle in vehicles if vehicle != cur_vehicle),
            key=lambda v: self._calculate_distance(cur_vehicle, v),
        )
        return nearest_vehicle

    @staticmethod
    def _calculate_distance(vehicle1: Vehicle, vehicle2: Vehicle) -> float:
        distance = (
            math.acos(
                math.sin(math.radians(vehicle1.latitude))
                * math.sin(math.radians(vehicle2.latitude))
                + math.cos(math.radians(vehicle1.latitude))
                * math.cos(math.radians(vehicle2.latitude))
                * math.cos(math.radians(vehicle2.longitude - vehicle1.longitude))
            )
            * 6371
            * 1000
        )

        return distance  # type: ignore
