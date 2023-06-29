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

if __name__ == "__main__":
    app.run(debug=True)