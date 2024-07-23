import requests
from tests.conftest import ids, host, port
from tests.dataclasses import QuestionAnswerData


def test_flask_is_up():
    url = f"http://{host}:{port}/is_up"
    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"


def test_ask_endpoint():
    url = f"http://{host}:{port}/ask"
    headers = {"Content-Type": "application/json"}
    data = {"question": "How many strings there are in a philosopher?"}

    response = requests.post(url, headers=headers, json=data)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    ids.append(response.json()["id"])


def test_qa_endpoint():
    id = ids[0]
    url = f"http://{host}:{port}/qa/{id}"
    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert data["id"] == id, f"Unexpected id: {data['id']}"
    assert (
        data["question"] == "How many strings there are in a philosopher?"
    ), f"Unexpected question: {data['question']}"


def find_question(arr, id):
    for element in arr:
        if element["id"] == id:
            return element
    return None


def test_qas_endpoint():
    url = f"http://{host}:{port}/ask"
    headers = {"Content-Type": "application/json"}
    data = {"question": "Is there anybody in there?"}

    response = requests.post(url, headers=headers, json=data)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    ids.append(response.json()["id"])

    url = f"http://{host}:{port}/qas"
    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert len(data) >= 2, f"Unexpected number of questions: {len(data)}"

    obj = find_question(data, ids[0])
    q = QuestionAnswerData(obj["id"], obj["question"], obj["answer"])

    assert (
        q.question == "How many strings there are in a philosopher?"
    ), f"Unexpected question: { q.question}"

    obj = find_question(data, ids[1])
    q = QuestionAnswerData(obj["id"], obj["question"], obj["answer"])

    assert (
        q.question == "Is there anybody in there?"
    ), f"Unexpected question: { q.question}"
