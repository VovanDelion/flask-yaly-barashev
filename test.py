import  requests


def test_jobs_api(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Good", resp.json())
    else:
        print(resp.status_code, resp.text)

test_jobs_api(requests.get("localhost:8080/api/jobs").json())
test_jobs_api(requests.get("localhost:8080/api/jobs/2").json())
