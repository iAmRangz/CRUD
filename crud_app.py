from flask import Flask, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345678ten"
app.config["MYSQL_DB"] = "employees"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


#index page
@app.route("/")
def index():
    return "Blank Homepage muna!"


@app.route("/employees", methods=["GET"])
def get_all_employees():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM employees""")
    rv = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>", methods=["GET"])
def get_employee_by_employee_number(emp_no):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM employees WHERE emp_no = %s""", (emp_no,))
    rv = cur.fetchall()
    cur.close()

    return make_response(jsonify(rv), 200)


@app.route("/employees/<emp_no>/department", methods=["GET"])
def get_employee_department(emp_no):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.emp_no, e.first_name, e.last_name, d.dept_name
        FROM employees e
        JOIN dept_emp de ON e.emp_no = de.emp_no
        JOIN departments d ON de.dept_no = d.dept_no
        WHERE e.emp_no = %s AND de.to_date > NOW()
        """, [emp_no])
    rv = cur.fetchall()
    cur.close()

    return make_response(jsonify(rv), 200)


@app.route("/departments/<dept_no>/managers", methods=["GET"])
def get_department_managers(dept_no):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.dept_no, d.dept_name, e.emp_no, e.first_name, e.last_name
        FROM dept_manager dm
        JOIN departments d ON dm.dept_no = d.dept_no
        JOIN employees e ON dm.emp_no = e.emp_no
        WHERE d.dept_no = %s
        """, [dept_no])
    rv = cur.fetchall()
    cur.close()

    return make_response(jsonify(rv), 200)


if __name__ == "__main__":
    app.run(debug=True)