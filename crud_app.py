from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL

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
    return "Blank Homepage muna!"


@app.route("/employees", methods=["GET"])
def get_all_employees():
    rv = execute_query("SELECT * FROM employees")
    if "error" in rv:
        return make_response(jsonify({"error": "Database error"}), 500)
    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>", methods=["GET"])
def get_employee_by_employee_number(emp_no):
    rv = execute_query("SELECT * FROM employees WHERE emp_no = %s", (emp_no,))
    if "error" in rv:
        return make_response(jsonify({"error": "Database error"}), 500)
    return make_response(jsonify(rv), 200)


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
        return make_response(jsonify({"error": "Database error"}), 500)
    return make_response(jsonify(rv), 200)


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
        return make_response(jsonify({"error": "Database error"}), 500)
    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>/salaries", methods=["GET"])
def get_employee_salaries(emp_no):
    rv = execute_query("""
        SELECT e.emp_no, e.first_name, e.last_name, s.salary, s.from_date, s.to_date
        FROM employees e
        JOIN salaries s ON e.emp_no = s.emp_no
        WHERE e.emp_no = %s
        """, [emp_no])
    if "error" in rv:
        return make_response(jsonify({"error": "Database error"}), 500)
    return make_response(jsonify(rv), 200)


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.json
    required_fields = ["first_name", "last_name", "hire_date", "gender", "birth_date"]
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required field"}), 400)

    try:
        execute_query("INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)",
                      (data["first_name"], data["last_name"], data["hire_date"], data["gender"], data["birth_date"]))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    return make_response(jsonify({"result": "Employee created"}), 201)


@app.route("/employees/<emp_no>", methods=["PUT"])
def update_employee(emp_no):
    data = request.json
    if not employee_exists(emp_no):
        return make_response(jsonify({"error": "Employee not found"}), 404)

    try:
        execute_query("""UPDATE employees SET first_name = %s, last_name = %s WHERE emp_no = %s""",
                      (data["first_name"], data["last_name"], emp_no))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    return make_response(jsonify({"result": "Employee updated"}), 200)


@app.route("/employees/<emp_no>", methods=["DELETE"])
def delete_employee(emp_no):
    if not employee_exists(emp_no):
        return make_response(jsonify({"error": "Employee not found"}), 404)

    try:
        execute_query("""DELETE FROM employees WHERE emp_no = %s""", [emp_no])
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    return make_response(jsonify({"result": "Employee deleted"}), 200)


if __name__ == "__main__":
    app.run(debug=True)