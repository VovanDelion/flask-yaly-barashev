import pytest
import requests


BASE_URL = "localhost:8080"

def test_jobs_api(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Good", resp.json())
    else:
        print(resp.status_code, resp.text)


def test_delete_job():
    response = requests.get(f"{BASE_URL}/api/jobs")
    assert response.status_code == 200
    initial_jobs = response.json()["jobs"]
    assert len(initial_jobs) > 0

    job_to_delete = initial_jobs[0]
    job_id = job_to_delete["id"]

    delete_response = requests.delete(f"{BASE_URL}/api/jobs/delete/{job_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["success"] == f"Job {job_id} deleted"

    response_after_delete = requests.get(f"{BASE_URL}/api/jobs/")
    assert response_after_delete.status_code == 200
    remaining_jobs = response_after_delete.json()["jobs"]
    assert len(remaining_jobs) == len(initial_jobs) - 1
    assert all(job["id"] != job_id for job in remaining_jobs)


@pytest.fixture
def test_job():
    new_job = {
        "job": "Original job",
        "work_size": 10,
        "collaborators": "1,2,3",
        "is_finished": False,
        "team_leader": 1
    }
    response = requests.post(f"{BASE_URL}/api/jobs/edit", json=new_job)
    job_id = response.json().get("ok")
    yield job_id
    requests.delete(f"{BASE_URL}/api/jobs/edit/{job_id}")


def test_successful_job_edit(test_job):
    initial_response = requests.get(f"{BASE_URL}/api/jobs/edit/{test_job}")
    initial_data = initial_response.json()["job"]

    update_data = {
        "job": "Updated job title",
        "work_size": 20,
        "is_finished": True
    }

    edit_response = requests.put(f"{BASE_URL}/api/jobs/edit/{test_job}", json=update_data)
    assert edit_response.status_code == 200

    updated_job = edit_response.json()["job"]
    assert updated_job["job"] == "Updated job title"
    assert updated_job["work_size"] == 20
    assert updated_job["is_finished"] is True
    assert updated_job["collaborators"] == initial_data["collaborators"]

    all_jobs_response = requests.get(f"{BASE_URL}/api/jobs/edit")
    all_jobs = all_jobs_response.json()["jobs"]
    edited_job_in_list = next((job for job in all_jobs if job["id"] == test_job), None)
    assert edited_job_in_list is not None
    assert edited_job_in_list["job"] == "Updated job title"

test_jobs_api(requests.get("localhost:8080/api/jobs").json())
test_jobs_api(requests.get("localhost:8080/api/jobs/2").json())
