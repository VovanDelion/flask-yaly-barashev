import unittest
import json
from flask import Flask
from flask_restful import Api
from app.models.db_session import db_session, global_init
from app.models.job import Job
from app.models.user import User
from app.resources.jobs_resource import JobsResource, JobsListResource


app = Flask(__name__)
api = Api(app)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(JobsListResource, '/api/v2/jobs')
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')


class TestJobsAPI(unittest.TestCase):
    def setUp(self):
        global_init("sqlite:///:memory:")
        self.session = db_session.create_session()
        self.client = app.test_client()

        self.team_leader = User(
            surname="Leader",
            name="Test",
            age=40,
            position="Chief",
            speciality="Management",
            address="Mars Base 1",
            email="leader@mars.org"
        )
        self.session.add(self.team_leader)
        self.session.commit()

        test_job = Job(
            team_leader=self.team_leader.id,
            job="Build new habitat",
            work_size=15,
            collaborators="2, 3, 5",
            is_finished=False
        )
        self.session.add(test_job)
        self.session.commit()
        self.test_job_id = test_job.id

    def tearDown(self):
        self.session.close()

    def test_get_all_jobs_correct(self):
        response = self.client.get('/api/v2/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('jobs', data)
        self.assertTrue(isinstance(data['jobs'], list))
        self.assertEqual(len(data['jobs']), 1)

    def test_post_job_correct(self):
        new_job_data = {
            'team_leader': self.team_leader.id,
            'job': 'Deploy solar panels',
            'work_size': 10,
            'collaborators': '4, 6',
            'is_finished': False
        }
        response = self.client.post(
            '/api/v2/jobs',
            data=json.dumps(new_job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

        response = self.client.get('/api/v2/jobs')
        data = json.loads(response.data)
        self.assertEqual(len(data['jobs']), 2)

    def test_post_job_missing_required_field(self):
        incomplete_job_data = {
            'team_leader': self.team_leader.id,
            'job': 'Incomplete job',
        }
        response = self.client.post(
            '/api/v2/jobs',
            data=json.dumps(incomplete_job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_job_invalid_team_leader(self):
        invalid_job_data = {
            'team_leader': 9999,
            'job': 'Invalid job',
            'work_size': 5,
            'collaborators': '1'
        }
        response = self.client.post(
            '/api/v2/jobs',
            data=json.dumps(invalid_job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_job_correct(self):
        response = self.client.get(f'/api/v2/jobs/{self.test_job_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('job', data)
        self.assertEqual(data['job']['job'], 'Build new habitat')

    def test_get_job_not_found(self):
        response = self.client.get('/api/v2/jobs/9999')
        self.assertEqual(response.status_code, 404)

    def test_put_job_correct(self):
        update_data = {
            'team_leader': self.team_leader.id,
            'job': 'Updated job description',
            'work_size': 20,
            'collaborators': '2, 4, 6',
            'is_finished': True
        }
        response = self.client.put(
            f'/api/v2/jobs/{self.test_job_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v2/jobs/{self.test_job_id}')
        data = json.loads(response.data)
        self.assertEqual(data['job']['job'], 'Updated job description')
        self.assertTrue(data['job']['is_finished'])

    def test_put_job_invalid_data(self):
        invalid_update = {
            'team_leader': 'not_an_integer',
            'job': '',
            'work_size': -5
        }
        response = self.client.put(
            f'/api/v2/jobs/{self.test_job_id}',
            data=json.dumps(invalid_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_job_correct(self):
        response = self.client.delete(f'/api/v2/jobs/{self.test_job_id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v2/jobs/{self.test_job_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_job_not_found(self):
        response = self.client.delete('/api/v2/jobs/9999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()