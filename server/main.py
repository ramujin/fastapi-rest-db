''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
from fastapi import FastAPI, Request              # The main FastAPI import and Request object
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.templating import Jinja2Templates    # Used for generating HTML from templatized files
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
import uvicorn                                    # Used for running the app directly through Python
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

app = FastAPI()                                   # Specify the "app" that will run the routing
views = Jinja2Templates(directory="views")        # Specify where the HTML files are located
static_files = StaticFiles(directory="public")    # Specify where the static files are located
app.mount("/public", static_files, name="public") # Mount the static files directory to /public

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
# CREATE SQL query
def db_create_user(first_name:str, last_name:str) -> int:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("insert into users (first_name, last_name) values (%s, %s)", (first_name, last_name))
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def db_select_users(user_id:int=None) -> list:
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
def db_update_user(user_id:int, first_name:str, last_name:str) -> bool:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "update users set first_name=%s, last_name=%s where id=%s;"
  values = (first_name, last_name, user_id)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def db_delete_user(user_id:int) -> bool:
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"delete from users where id={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# GET /
# Home route to load the main page
@app.get("/", response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  with open("views/index.html") as html:
    return views.TemplateResponse("index.html", {"request":request, "users":db_select_users()})

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# RESTful User Routes

# GET /user
# Used to query a single user RESTfully
@app.get('/user/{user_id}')
def get_user(user_id:int) -> dict:
  user = db_select_users(user_id)
  response = {} if user==None else {'id':user[0], 'first_name':user[1], 'last_name':user[2]}
  return response

# POST /user
# Used to create a new user
@app.post("/user")
async def post_user(request:Request) -> dict:
  data = await request.json()
  first_name, last_name = data['first_name'], data['last_name']
  new_id = db_create_user(first_name, last_name)

  # Send the new record back
  return get_user(new_id)

# PUT /user
@app.put('/user/{user_id}')
async def put_user(user_id:int, request:Request) -> dict:
  data = await request.json()
  first_name, last_name = data['first_name'], data['last_name']
  return {'success': db_update_user(user_id, first_name, last_name)}

# DELETE /user
@app.delete('/user/{user_id}')
def delete_user(user_id:int) -> dict:
  return {'success': db_delete_user(user_id)}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If running the server directly from Python as a module
if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)