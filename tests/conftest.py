import pytest
import requests

# If you change the port or host, make sure to change it in the test as well
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
