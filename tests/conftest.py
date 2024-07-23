import pytest
import requests

# TODO
port = 80
host = "localhost"

ids = []


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    for id in ids:
        url = f"http://{host}:{port}/qa/{id}"
        response = requests.delete(url)
        assert (
            response.status_code == 200
        ), f"Failed to delete id {id}, status code: {response.status_code}"
