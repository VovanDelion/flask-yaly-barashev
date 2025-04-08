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

    response_after_delete = requests.get(f"{BASE_URL}/api/jobs")
    assert response_after_delete.status_code == 200
    remaining_jobs = response_after_delete.json()["jobs"]
    assert len(remaining_jobs) == len(initial_jobs) - 1
    assert all(job["id"] != job_id for job in remaining_jobs)

test_jobs_api(requests.get("localhost:8080/api/jobs").json())
test_jobs_api(requests.get("localhost:8080/api/jobs/2").json())
