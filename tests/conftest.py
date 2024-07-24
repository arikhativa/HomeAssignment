import time
import pytest
import requests

# If you change the port or host, make sure to change it in the test as well
port = 80
host = "localhost"

ids = []


def test_flask_is_up(retries=5, delay=2):
    url = f"http://{host}:{port}/is_up"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Flask is up!")
                return
        except requests.ConnectionError:
            print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise AssertionError("Flask is not up after several attempts.")


def pytest_sessionstart(session):
    try:
        test_flask_is_up()
    except AssertionError as e:
        pytest.exit(str(e))


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    for id in ids:
        url = f"http://{host}:{port}/qa/{id}"
        response = requests.delete(url)
        assert (
            response.status_code == 200
        ), f"Failed to delete id {id}, status code: {response.status_code}"
