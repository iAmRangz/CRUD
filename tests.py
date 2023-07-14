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
    
    # Ang tagal matapos ng test dahil dito. ^_^
    def test_get_all_employees_json(self):
        response = self.app.get("/employees")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Georgi", response.data)
    
    def test_get_all_employees_xml(self):
        response = self.app.get("/employees?format=xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<first_name type=\"str\">Georgi</first_name>", response.data)
    
    def test_get_employee_by_employee_number_json(self):
        response = self.app.get("/employees/10069")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Margareta", response.data)
        self.assertNotIn(b"Georgi", response.data)
        
    def test_get_employee_by_employee_number_xml(self):
        response = self.app.get("/employees/10069?format=xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<first_name type=\"str\">Margareta</first_name>", response.data)
        self.assertNotIn(b"<first_name type=\"str\">Georgi</first_name>", response.data)
    
    def test_get_employee_department_json(self):
        response = self.app.get("/employees/10069/department")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Production", response.data)
        self.assertNotIn(b"Sales", response.data)
        
    def test_get_employee_department_xml(self):
        response = self.app.get("/employees/10069/department?format=xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<dept_name type=\"str\">Production</dept_name>", response.data)
        self.assertNotIn(b"<dept_name type=\"str\">Sales</dept_name>", response.data)

    def test_get_department_managers_json(self):
        response = self.app.get("/departments/d004/managers")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Oscar", response.data)
        self.assertNotIn(b"Peternela", response.data)
        
    def test_get_department_managers_xml(self):
        response = self.app.get("/departments/d004/managers?format=xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<first_name type=\"str\">Oscar</first_name>", response.data)
        self.assertNotIn(b"<first_name type=\"str\">Peternela</first_name>", response.data)

    def test_get_employee_salaries_json(self):
        response = self.app.get("/employees/110420/salaries")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"53978", response.data)
        self.assertNotIn(b"50000", response.data)
        
    def test_get_employee_salaries_xml(self):
        response = self.app.get("/employees/110420/salaries?format=xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<salary type=\"int\">53978</salary>", response.data)
        self.assertNotIn(b"<salary type=\"int\">50000</salary>", response.data)

    def test_create_and_update_employee(self):
        new_employee = {
            "emp_no": "69",
            "first_name": "Naruto",
            "last_name": "Uzumaki",
            "hire_date": "2023-07-01",
            "gender": "M",
            "birth_date": "1990-01-01"
        }
        response = self.app.post("/employees", 
                                data=json.dumps(new_employee),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Employee created", response.data)
        
        update_employee = {
            "first_name": "Buruto",
            "last_name": "Uzumaki",
        }
        response = self.app.put("/employees/69", 
                                data=json.dumps(update_employee),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee updated", response.data)


    def test_delete_employee(self):
        response = self.app.delete("/employees/69")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee deleted", response.data)

if __name__ == "__main__":
    unittest.main()
