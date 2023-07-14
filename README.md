# Employee Management API

## Description
This project is a CRUD (Create, Read, Update, Delete) API for managing employee data. Built with Python and Flask, the API interacts with the employees database from MySQL, allowing the user to manipulate and access data related to employees, their departments, and salaries.

## Data Source
This application uses the MySQL "employees" database as its primary data source. More information about this database and its schema can be found [here](https://dev.mysql.com/doc/employee/en/).

## Installation
To get started with the Employee Management API, follow these steps:

```bash
# clone the repository
git clone https://github.com/iAmRangz/CRUD.git

# navigate into the project directory
cd CRUD

# install the dependencies
pip install -r requirements.txt



Database Configuration
The application is configured to interact with a MySQL database server running on localhost. The default configuration is as follows:
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "yourpassword"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

Please make sure to update the MYSQL_PASSWORD with your actual MySQL root password before running the application.


Usage
Running the application is straightforward:
cd CRUD
python crud_app.py


The server will start, typically on http://localhost:5000. You can then access the API endpoints through this server.
