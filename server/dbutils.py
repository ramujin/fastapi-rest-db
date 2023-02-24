''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('../credentials.env')                 # Read in the environment variables for MySQL
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
# CREATE SQL query
def create_user(first_name:str, last_name:str) -> int:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("insert into users (first_name, last_name) values (%s, %s)", (first_name, last_name))
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  if user_id == None:
    query = f"select id, first_name, last_name from users;"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select id, first_name, last_name from users where id={user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
  db.close()
  return result

# UPDATE SQL query
def update_user(user_id:int, first_name:str, last_name:str) -> bool:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "update users set first_name=%s, last_name=%s where id=%s;"
  values = (first_name, last_name, user_id)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_id:int) -> bool:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"delete from users where id={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False
