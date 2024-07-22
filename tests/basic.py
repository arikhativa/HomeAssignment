import requests
import pytest

# TODO use .end as port
port = 80
ids = []


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    for id in ids:
        url = f"http://localhost:{port}/qa/{id}"
        response = requests.delete(url)
        assert (
            response.status_code == 200
        ), f"Failed to delete id {id}, status code: {response.status_code}"


def test_flask_is_up():
    url = f"http://localhost:{port}/is_up"
    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"


def test_ask_endpoint():
    url = f"http://localhost:{port}/ask"
    headers = {"Content-Type": "application/json"}
    data = {"question": "How many strings there are in a philosopher?"}

    response = requests.post(url, headers=headers, json=data)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    ids.append(response.json()["id"])


# def test_qa_endpoint():
#     url = f"http://localhost:{port}/qa/1"
#     response = requests.get(url)
#     assert (
#         response.status_code == 200
#     ), f"Expected status code 200, but got {response.status_code}"

#     data = response.json()
#     assert data["id"] == ids[0], f"Unexpected id: {data['id']}"
#     assert (
#         data["question"] == "How many strings there are in a philosopher?"
#     ), f"Unexpected question: {data['question']}"


# def test_qas_endpoint():
#     url = f"http://localhost:{port}/ask"
#     headers = {"Content-Type": "application/json"}
#     data = {"question": "Is there anybody in there?"}

#     response = requests.post(url, headers=headers, json=data)
#     assert (
#         response.status_code == 201
#     ), f"Expected status code 201, but got {response.status_code}"

#     ids.append(response.json()["id"])

#     url = f"http://localhost:{port}/qas"
#     response = requests.get(url)
#     assert (
#         response.status_code == 200
#     ), f"Expected status code 200, but got {response.status_code}"

#     data = response.json()
#     assert len(data) == 2, f"Unexpected number of questions: {len(data)}"
#     assert (
#         data[1]["question"] == "Is there anybody in there?"
#     ), f"Unexpected question: {data[1]['question']}"
#     assert data[1]["answer"] == "answer", f"Unexpected answer: {data[1]['answer']}"
