from typing import Any

import requests

from src import exeptions as e


class API:
    def __init__(self, url: str, timeout: int) -> None:
        self.url = url
        self.timeout = timeout
        self.session = requests.Session()

    def get_list(self) -> list[dict[str, Any]]:
        try:
            response = self.session.get(url=f"{self.url}/vehicles", timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise e.VehicleManagerAPIError(str(err)) from err

        try:
            return response.json()  # type: ignore
        except requests.JSONDecodeError as err:
            raise e.VehiclesInavlidResponseError(str(err)) from err

    def get(self, vehicle_id: int) -> dict[str, Any]:
        try:
            response = self.session.get(
                url=f"{self.url}/vehicles/{vehicle_id}", timeout=self.timeout
            )
            if response.status_code == 404:
                raise e.VehicleNotFoundError(f"'Vehicle' object not found with id={vehicle_id}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise e.VehicleManagerAPIError(str(err)) from err

        try:
            return response.json()  # type: ignore
        except requests.JSONDecodeError as err:
            raise e.VehiclesInavlidResponseError(str(err)) from err

    def create(self, vehicle: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self.session.post(
                url=f"{self.url}/vehicles",
                json=vehicle,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise e.VehicleManagerAPIError(str(err)) from err

        try:
            return response.json()  # type: ignore
        except requests.JSONDecodeError as err:
            raise e.VehiclesInavlidResponseError(str(err)) from err

    def update(self, vehicle_id: int, vehicle: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self.session.put(
                url=f"{self.url}/vehicles/{vehicle_id}",
                json=vehicle,
                timeout=self.timeout,
            )
            if response.status_code == 404:
                raise e.VehicleNotFoundError(f"'Vehicle' object not found with id={vehicle_id}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise e.VehicleManagerAPIError(str(err)) from err
        try:
            return response.json()  # type: ignore
        except requests.JSONDecodeError as err:
            raise e.VehiclesInavlidResponseError(str(err)) from err

    def delete(self, vehicle_id: int) -> None:
        try:
            response = self.session.delete(
                url=f"{self.url}/vehicles/{vehicle_id}",
                timeout=self.timeout,
            )
            if response.status_code == 404:
                raise e.VehicleNotFoundError(f"'Vehicle' object not found with id={vehicle_id}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise e.VehicleManagerAPIError(str(err)) from err
