import pytest
from requests_mock import Mocker as RequestsMocker

from src.exeptions import VehicleNotFoundError
from src.models import Vehicle
from src.vehicle_manager import VehicleManager


@pytest.fixture()
def base_url(environ: dict[str, str]) -> str:
    return environ["VEHICELS_API_URL"]


@pytest.fixture()
def manager(base_url: str, requests_mock: RequestsMocker) -> VehicleManager:
    return VehicleManager(url=base_url)


def test_get_vehicles(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[
            {
                "id": 1,
                "name": "Toyota",
                "model": "Camry",
                "year": 2021,
                "color": "red",
                "price": 21000,
                "latitude": 55.753332,
                "longitude": 37.621676,
            },
            {
                "id": 2,
                "name": "BMW",
                "model": "X5",
                "year": 2015,
                "color": "black",
                "price": 20000,
                "latitude": 59.986607,
                "longitude": 30.321435,
            },
        ],
    )
    expected = [
        Vehicle(
            id=1,
            name="Toyota",
            model="Camry",
            year=2021,
            color="red",
            price=21000,
            latitude=55.753332,
            longitude=37.621676,
        ),
        Vehicle(
            id=2,
            name="BMW",
            model="X5",
            year=2015,
            color="black",
            price=20000,
            latitude=59.986607,
            longitude=30.321435,
        ),
    ]
    assert manager.get_vehicles() == expected


def test_get_vehicles__empty_response(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[],
    )
    assert manager.get_vehicles() == []


def test_filter_vehicles(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[
            {
                "id": 1,
                "name": "Toyota",
                "model": "Camry",
                "year": 2021,
                "color": "red",
                "price": 21000,
                "latitude": 55.753332,
                "longitude": 37.621676,
            },
            {
                "id": 2,
                "name": "BMW",
                "model": "X5",
                "year": 2015,
                "color": "black",
                "price": 20000,
                "latitude": 59.986607,
                "longitude": 30.321435,
            },
        ],
    )

    expected = [
        Vehicle(
            id=1,
            name="Toyota",
            model="Camry",
            year=2021,
            color="red",
            price=21000,
            latitude=55.753332,
            longitude=37.621676,
        ),
    ]
    assert manager.filter_vehicles(params={"name": "Toyota", "year": 2021}) == expected


def test_filter_vehicles__empty_response(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[],
    )

    assert manager.filter_vehicles(params={"name": "Toyota", "year": 2021}) == []


def test_filter_vehicles__no_params(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[
            {
                "id": 1,
                "name": "Toyota",
                "model": "Camry",
                "year": 2021,
                "color": "red",
                "price": 21000,
                "latitude": 55.753332,
                "longitude": 37.621676,
            },
            {
                "id": 2,
                "name": "BMW",
                "model": "X5",
                "year": 2015,
                "color": "black",
                "price": 20000,
                "latitude": 59.986607,
                "longitude": 30.321435,
            },
        ],
    )

    expected = [
        Vehicle(
            id=1,
            name="Toyota",
            model="Camry",
            year=2021,
            color="red",
            price=21000,
            latitude=55.753332,
            longitude=37.621676,
        ),
        Vehicle(
            id=2,
            name="BMW",
            model="X5",
            year=2015,
            color="black",
            price=20000,
            latitude=59.986607,
            longitude=30.321435,
        ),
    ]
    assert manager.filter_vehicles(params={}) == expected


def test_filter_vehicles__param_not_in_vehicle_attrs(
    manager: VehicleManager,
) -> None:
    with pytest.raises(AttributeError, match="'Vehicle' object has no attributes:"):
        manager.filter_vehicles(params={"type": "sedan"})


def test_filter_vehicles__param_value_not_valid(
    manager: VehicleManager,
) -> None:
    with pytest.raises(
        TypeError, match="'Vehicle.year' has type <class 'int'> received <class 'str'>"
    ):
        manager.filter_vehicles(params={"year": "hello"})


def test_get_vehicle(base_url: str, manager: VehicleManager, requests_mock: RequestsMocker) -> None:
    car_id = 1
    requests_mock.get(
        url=f"{base_url}/vehicles/{car_id}",
        json={
            "id": 1,
            "name": "Toyota",
            "model": "Camry",
            "year": 2021,
            "color": "red",
            "price": 21000,
            "latitude": 55.753332,
            "longitude": 37.621676,
        },
    )

    expected = Vehicle(
        id=1,
        name="Toyota",
        model="Camry",
        year=2021,
        color="red",
        price=21000,
        latitude=55.753332,
        longitude=37.621676,
    )

    assert manager.get_vehicle(vehicle_id=1) == expected


def test_get_vehicle__not_found(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.get(
        url=f"{base_url}/vehicles/{car_id}",
        status_code=404,
        json={"error": "Vehicle not found"},
    )
    with pytest.raises(VehicleNotFoundError, match="'Vehicle' object not found with id=1"):
        manager.get_vehicle(vehicle_id=car_id)


def test_add_vehicle(base_url: str, manager: VehicleManager, requests_mock: RequestsMocker) -> None:
    requests_mock.post(
        url=f"{base_url}/vehicles",
        json={
            "id": 1,
            "name": "Mercedes",
            "model": "S500",
            "year": 2009,
            "color": "white",
            "price": 40000,
            "latitude": 59.950317,
            "longitude": 30.31799,
        },
    )
    data = {
        "name": "Mercedes",
        "model": "S500",
        "year": 2009,
        "color": "white",
        "price": 40000,
        "latitude": 59.950317,
        "longitude": 30.31799,
    }
    expected = Vehicle(
        id=1,
        name="Mercedes",
        model="S500",
        year=2009,
        color="white",
        price=40000,
        latitude=59.950317,
        longitude=30.31799,
    )
    assert manager.add_vehicle(vehicle=Vehicle.parse(data)) == expected


def test_update_vehicle(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.put(
        url=f"{base_url}/vehicles/{car_id}",
        json={
            "id": 1,
            "name": "Mercedes",
            "model": "S500",
            "year": 2009,
            "color": "white",
            "price": 40000,
            "latitude": 59.950317,
            "longitude": 30.31799,
        },
    )
    data = {
        "id": 1,
        "name": "Mercedes",
        "model": "S500",
        "year": 2009,
        "color": "white",
        "price": 40000,
        "latitude": 59.950317,
        "longitude": 30.31799,
    }
    expected = Vehicle(
        id=1,
        name="Mercedes",
        model="S500",
        year=2009,
        color="white",
        price=40000,
        latitude=59.950317,
        longitude=30.31799,
    )
    assert manager.update_vehicle(vehicle=Vehicle.parse(data)) == expected


def test_update_vehicle__not_found(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 2
    requests_mock.put(
        url=f"{base_url}/vehicles/{car_id}",
        json={"error": "Vehicle not found"},
        status_code=404,
    )
    data = {
        "id": 2,
        "name": "Mercedes",
        "model": "S500",
        "year": 2009,
        "color": "white",
        "price": 40000,
        "latitude": 59.950317,
        "longitude": 30.31799,
    }
    with pytest.raises(VehicleNotFoundError, match="'Vehicle' object not found with id=2"):
        manager.update_vehicle(vehicle=Vehicle.parse(data))


def test_update_vehicle__error_id_is_none(manager: VehicleManager) -> None:
    data = {
        "id": None,
        "name": "Mercedes",
        "model": "S500",
        "year": 2009,
        "color": "white",
        "price": 40000,
        "latitude": 59.950317,
        "longitude": 30.31799,
    }
    with pytest.raises(ValueError, match="'Vehicle' object attribute 'id' must be not None"):
        manager.update_vehicle(vehicle=Vehicle.parse(data))


def test_delete_vehicle(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.delete(
        url=f"{base_url}/vehicles/{car_id}",
        json={
            "id": 1,
            "name": "Mercedes",
            "model": "S500",
            "year": 2009,
            "color": "white",
            "price": 40000,
            "latitude": 59.950317,
            "longitude": 30.31799,
        },
    )
    manager.delete_vehicle(vehicle_id=car_id)


def test_delete_vehicle__not_found(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 2
    requests_mock.delete(
        url=f"{base_url}/vehicles/{car_id}",
        json={"error": "Vehicle not found"},
        status_code=404,
    )
    with pytest.raises(VehicleNotFoundError, match="'Vehicle' object not found with id=2"):
        manager.delete_vehicle(vehicle_id=car_id)


def test_get_distance(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car1_id = 1
    car2_id = 2

    requests_mock.get(
        url=f"{base_url}/vehicles/{car1_id}",
        json={
            "id": 1,
            "name": "Toyota",
            "model": "Camry",
            "year": 2021,
            "color": "red",
            "price": 21000,
            "latitude": 55.753332,
            "longitude": 37.621676,
        },
    )
    requests_mock.get(
        url=f"{base_url}/vehicles/{car2_id}",
        json={
            "id": 2,
            "name": "BMW",
            "model": "X5",
            "year": 2015,
            "color": "black",
            "price": 20000,
            "latitude": 59.986607,
            "longitude": 30.321435,
        },
    )

    assert manager.get_distance(id1=car1_id, id2=car2_id) == 638005.0864183326


def test_get_distance__not_found(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car1_id = 1
    car2_id = 2

    requests_mock.get(
        url=f"{base_url}/vehicles/{car1_id}",
        json={
            "id": 1,
            "name": "Toyota",
            "model": "Camry",
            "year": 2021,
            "color": "red",
            "price": 21000,
            "latitude": 55.753332,
            "longitude": 37.621676,
        },
    )
    requests_mock.get(
        url=f"{base_url}/vehicles/{car2_id}",
        status_code=404,
        json={"error": "Vehicle not found"},
    )
    with pytest.raises(VehicleNotFoundError, match="'Vehicle' object not found with id=2"):
        manager.get_distance(id1=car1_id, id2=car2_id)


def test_get_nearest_vehicle(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.get(
        url=f"{base_url}/vehicles/{car_id}",
        json={
            "id": 1,
            "name": "Toyota",
            "model": "Camry",
            "year": 2021,
            "color": "red",
            "price": 21000,
            "latitude": 55.753332,
            "longitude": 37.621676,
        },
    )

    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[
            {
                "id": 1,
                "name": "Toyota",
                "model": "Camry",
                "year": 2021,
                "color": "red",
                "price": 21000,
                "latitude": 55.753332,
                "longitude": 37.621676,
            },
            {
                "id": 2,
                "name": "BMW",
                "model": "X5",
                "year": 2015,
                "color": "black",
                "price": 20000,
                "latitude": 59.986607,
                "longitude": 30.321435,
            },
            {
                "id": 3,
                "name": "Mercedes",
                "model": "S500",
                "year": 2009,
                "color": "white",
                "price": 40000,
                "latitude": 59.950317,
                "longitude": 30.31799,
            },
        ],
    )
    expected = Vehicle(
        id=3,
        name="Mercedes",
        model="S500",
        year=2009,
        color="white",
        price=40000,
        latitude=59.950317,
        longitude=30.31799,
    )

    assert manager.get_nearest_vehicle(vehicle_id=car_id) == expected


def test_get_nearest_vehicle__with_one_vehicle(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.get(
        url=f"{base_url}/vehicles/{car_id}",
        json={
            "id": 1,
            "name": "Toyota",
            "model": "Camry",
            "year": 2021,
            "color": "red",
            "price": 21000,
            "latitude": 55.753332,
            "longitude": 37.621676,
        },
    )

    requests_mock.get(
        url=f"{base_url}/vehicles",
        json=[
            {
                "id": 1,
                "name": "Toyota",
                "model": "Camry",
                "year": 2021,
                "color": "red",
                "price": 21000,
                "latitude": 55.753332,
                "longitude": 37.621676,
            },
        ],
    )
    assert manager.get_nearest_vehicle(vehicle_id=car_id) is None


def test_get_nearest_vehicle__not_found(
    base_url: str, manager: VehicleManager, requests_mock: RequestsMocker
) -> None:
    car_id = 1
    requests_mock.get(
        url=f"{base_url}/vehicles/{car_id}",
        status_code=404,
        json={"error": "Vehicle not found"},
    )
    with pytest.raises(VehicleNotFoundError, match="'Vehicle' object not found with id=1"):
        manager.get_nearest_vehicle(vehicle_id=car_id)
