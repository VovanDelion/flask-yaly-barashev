import unittest
import json
from flask import Flask
from flask_restful import Api
from users_resource import UsersResource, UsersListResource
from data import db_session
from data.users import User

app = Flask(__name__)
api = Api(app)
app.config['TESTING'] = True

api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')

class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        self.session = db_session.create_session()
        self.client = app.test_client()

        test_user = User(
            surname="Test",
            name="User",
            age=30,
            position="Developer",
            speciality="Python",
            address="Test Address",
            email="test@example.com"
        )
        self.session.add(test_user)
        self.session.commit()
        self.test_user_id = test_user.id

    def tearDown(self):
        self.session.close()

    def test_get_all_users_correct(self):
        response = self.client.get('/api/v2/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('users', data)
        self.assertTrue(isinstance(data['users'], list))

    def test_post_user_correct(self):
        new_user_data = {
            'surname': 'New',
            'name': 'User',
            'age': 25,
            'position': 'Tester',
            'speciality': 'QA',
            'address': 'New Address',
            'email': 'new@example.com',
            'hashed_password': 'testpass'
        }
        response = self.client.post(
            '/api/v2/users',
            data=json.dumps(new_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_post_user_missing_field(self):
        incomplete_user_data = {
            'name': 'Incomplete',
            'age': 20
        }
        response = self.client.post(
            '/api/v2/users',
            data=json.dumps(incomplete_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_correct(self):
        response = self.client.get(f'/api/v2/users/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['surname'], 'Test')

    def test_get_user_not_found(self):
        response = self.client.get('/api/v2/users/9999')
        self.assertEqual(response.status_code, 404)

    def test_delete_user_correct(self):
        response = self.client.delete(f'/api/v2/users/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], 'OK')

        response = self.client.get(f'/api/v2/users/{self.test_user_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_user_not_found(self):
        response = self.client.delete('/api/v2/users/9999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()