import os
import unittest
import json

from app import create_app
import os
from github_query_params import MAX_PER_PAGE


class TrendingReposTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    ########## Tests ################
    def test_retrieve_all_tests(self):
        res = self.client().get('/trending_repos?repos_num=7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['repos']))

    def test_failed_response_if_repos_num_beyond_limit(self):
        res = self.client().get('/trending_repos?repos_num={}'.format(MAX_PER_PAGE + 1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
