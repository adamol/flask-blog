import unittest
from base import BaseTestCase

class IndexTest(BaseTestCase):

    def test_index_loads_correctly(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
