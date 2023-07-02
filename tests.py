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
        self.assertNotIn(b"Georgi", response.data)

    
    def test_get_employee_department(self):
        response = self.app.get("/employees/10069/department")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Production", response.data)
        self.assertNotIn(b"Sales", response.data)


    def test_get_department_managers(self):
        response = self.app.get("/departments/d004/managers")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Oscar", response.data)
        self.assertNotIn(b"Peternela", response.data)

if __name__ == "__main__":
    unittest.main()