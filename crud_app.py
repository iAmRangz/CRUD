from flask import Flask, jsonify, make_response, request, Response
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678ten"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def execute_query(query, params=None):
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, params)
        rv = cur.fetchall()
        cur.close()
        return rv
    except Exception as e:
        return {"error": str(e)}
    

def employee_exists(emp_no):
    rv = execute_query("SELECT * FROM employees WHERE emp_no = %s", [emp_no])
    return len(rv) > 0


@app.route("/")
def index():
    return """
    <h1>Welcome to the Employee Management API!</h1>
    <p>Here are some available endpoints:</p>
    <ul>
        <li><b>GET /employees:</b> Returns a list of all employees</li>
        <li><b>GET /employees/&lt;emp_no&gt;:</b> Returns the details of an employee by employee number</li>
        <li><b>GET /employees/&lt;emp_no&gt;/department:</b> Returns the department of an employee</li>
        <li><b>GET /departments/&lt;dept_no&gt;/managers:</b> Returns the managers of a department</li>
        <li><b>GET /employees/&lt;emp_no&gt;/salaries:</b> Returns the salaries of an employee</li>
        <li><b>GET /employees/search?name=&lt;name&gt;:</b> Search for an employee by their first name or last name</li>
        <li><b>GET /titles/&lt;title&gt;/employees:</b> Returns a list of employees who have held a certain title</li>
        <li><b>POST /employees:</b> Create a new employee</li>
        <li><b>PUT /employees/&lt;emp_no&gt;:</b> Update an employee's details</li>
        <li><b>DELETE /employees/&lt;emp_no&gt;:</b> Delete an employee</li>
    </ul>
    """


def format_response(data, status_code=200):
    """Formats the response as XML or JSON."""
    response_format = request.args.get('format', default='json', type=str)
    if response_format == 'xml':
        xml = dicttoxml(data)
        return Response(xml, mimetype='text/xml', status=status_code)
    else:  # Default to JSON
        return make_response(jsonify(data), status_code)
    

@app.route("/employees", methods=["GET"])
def get_all_employees():
    rv = execute_query("SELECT * FROM employees")
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    return format_response(rv, 200)


@app.route("/employees/<emp_no>", methods=["GET"])
def get_employee_by_employee_number(emp_no):
    rv = execute_query("SELECT * FROM employees WHERE emp_no = %s", (emp_no,))
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Employee not found"}, 404)
    return format_response(rv, 200)


@app.route("/employees/<emp_no>/department", methods=["GET"])
def get_employee_department(emp_no):
    rv = execute_query("""
        SELECT e.emp_no, e.first_name, e.last_name, d.dept_name
        FROM employees e
        JOIN dept_emp de ON e.emp_no = de.emp_no
        JOIN departments d ON de.dept_no = d.dept_no
        WHERE e.emp_no = %s AND de.to_date > NOW()
        """, [emp_no])
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Employee not found"}, 404)
    return format_response(rv, 200)


@app.route("/departments/<dept_no>/managers", methods=["GET"])
def get_department_managers(dept_no):
    rv = execute_query("""
        SELECT d.dept_no, d.dept_name, e.emp_no, e.first_name, e.last_name
        FROM dept_manager dm
        JOIN departments d ON dm.dept_no = d.dept_no
        JOIN employees e ON dm.emp_no = e.emp_no
        WHERE d.dept_no = %s
        """, [dept_no])
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Department not found"}, 404)
    return format_response(rv, 200)


@app.route("/employees/<emp_no>/salaries", methods=["GET"])
def get_employee_salaries(emp_no):
    rv = execute_query("""
        SELECT e.emp_no, e.first_name, e.last_name, s.salary, s.from_date, s.to_date
        FROM employees e
        JOIN salaries s ON e.emp_no = s.emp_no
        WHERE e.emp_no = %s
        """, [emp_no])
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Employee not found"}, 404)
    return format_response(rv, 200)


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.json
    required_fields = ["emp_no", "first_name", "last_name", "hire_date", "gender", "birth_date"]
    if not all(field in data for field in required_fields):
        return format_response({"error": "Missing required field"}, 400)

    try:
        result = execute_query("INSERT INTO employees (emp_no, first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s, %s)",
                               (data["emp_no"], data["first_name"], data["last_name"], data["hire_date"], data["gender"], data["birth_date"]))
        if "error" in result:
            raise Exception(result["error"])
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return format_response({"error": str(e)}, 500)
    return format_response({"result": "Employee created"}, 201)


@app.route("/employees/<emp_no>", methods=["PUT"])
def update_employee(emp_no):
    data = request.json
    if not employee_exists(emp_no):
        return format_response({"error": "Employee not found"}, 404)

    try:
        execute_query("""UPDATE employees SET first_name = %s, last_name = %s WHERE emp_no = %s""",
                      (data["first_name"], data["last_name"], emp_no))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return format_response({"error": str(e)}, 500)
    return format_response({"result": "Employee updated"}, 200)


@app.route("/employees/<emp_no>", methods=["DELETE"])
def delete_employee(emp_no):
    if not employee_exists(emp_no):
        return format_response({"error": "Employee not found"}, 404)

    try:
        execute_query("""DELETE FROM employees WHERE emp_no = %s""", [emp_no])
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return format_response({"error": str(e)}, 500)
    return format_response({"result": "Employee deleted"}, 200)


@app.route("/employees/search", methods=["GET"])
def search_employee_by_name():
    name = request.args.get('name')
    if not name:
        return format_response({"error": "Missing parameter 'name'"}, 400)
    rv = execute_query("SELECT * FROM employees WHERE first_name LIKE %s OR last_name LIKE %s", (f"%{name}%", f"%{name}%"))
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Employee not found"}, 404)
    return format_response(rv, 200)


@app.route("/titles/<title>/employees", methods=["GET"])
def get_employees_by_title(title):
    rv = execute_query("""
        SELECT e.emp_no, e.first_name, e.last_name
        FROM employees e
        JOIN titles t ON e.emp_no = t.emp_no
        WHERE t.title = %s
        """, [title])
    if "error" in rv:
        return format_response({"error": "Database error"}, 500)
    if not rv:
        return format_response({"error": "Title not found"}, 404)
    return format_response(rv, 200)


if __name__ == "__main__":
    app.run(debug=True)