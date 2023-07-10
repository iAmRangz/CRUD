import unittest
import warnings
import json
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


    def test_get_employee_salaries(self):
        response = self.app.get("/employees/110420/salaries")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"53978", response.data)
        self.assertNotIn(b"50000", response.data)


    def test_create_employee(self):
        new_employee = {
            "first_name": "Test",
            "last_name": "Employee",
            "hire_date": "2023-07-01",
            "gender": "M",
            "birth_date": "1990-01-01"
        }
        response = self.app.post("/employees", 
                                data=json.dumps(new_employee),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Employee created", response.data)


    def test_update_employee(self):
        update_employee = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = self.app.put("/employees/1", 
                                data=json.dumps(update_employee),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee updated", response.data)

    def test_delete_employee(self):
        response = self.app.delete("/employees/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee deleted", response.data)


if __name__ == "__main__":
    unittest.main()