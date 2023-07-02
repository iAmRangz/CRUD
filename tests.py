import unittest
import warnings
from crud_app import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

        
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blank Homepage muna!", response.data)
        

    def test_get_all_employees(self):
        response = self.app.get("/employees")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Georgi", response.data)

    
    def test_get_employee_by_employee_number(self):
        response = self.app.get("/employees/10069")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Margareta", response.data)

if __name__ == "__main__":
    unittest.main()