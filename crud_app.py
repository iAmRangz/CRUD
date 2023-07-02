from flask import Flask, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678ten"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def execute_query(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    rv = cur.fetchall()
    cur.close()
    return rv


@app.route("/")
def index():
    return "Blank Homepage muna!"


@app.route("/employees", methods=["GET"])
def get_all_employees():
    rv = execute_query("SELECT * FROM employees")
    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>", methods=["GET"])
def get_employee_by_employee_number(emp_no):
    rv = execute_query("SELECT * FROM employees WHERE emp_no = %s", (emp_no,))
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
    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>/salaries", methods=["GET"])
def get_employee_salaries(emp_no):
    rv = execute_query("""
        SELECT e.emp_no, e.first_name, e.last_name, s.salary, s.from_date, s.to_date
        FROM employees e
        JOIN salaries s ON e.emp_no = s.emp_no
        WHERE e.emp_no = %s
        """, [emp_no])
    return make_response(jsonify(rv), 200)


if __name__ == "__main__":
    app.run(debug=True)
