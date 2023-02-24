''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
from fastapi import FastAPI, Request              # The main FastAPI import and Request object
from pydantic import BaseModel                    # Used to define the model matching the DB Schema
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.templating import Jinja2Templates    # Used for generating HTML from templatized files
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
import uvicorn                                    # Used for running the app directly through Python
import dbutils as db                              # Import helper module of database functions!

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
app = FastAPI()                                   # Specify the "app" that will run the routing
views = Jinja2Templates(directory='views')        # Specify where the HTML files are located
static_files = StaticFiles(directory='public')    # Specify where the static files are located
app.mount('/public', static_files, name='public') # Mount the static files directory to /public

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define a User class that matches the SQL schema we defined for our users
class User(BaseModel):
  first_name: str
  last_name: str

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Home route to load the main page in a templatized fashion

# GET /
@app.get('/', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  return views.TemplateResponse('index.html', {'request':request, 'users':db.select_users()})

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# RESTful User Routes

# GET /users
# Used to query a collection of all users
@app.get('/users')
def get_users() -> dict:
  users = db.select_users()
  keys = ['id', 'first_name', 'last_name']
  users = [dict(zip(keys, user)) for user in users]
  return {"users": users}

# GET /users/{user_id}
# Used to query a single user
@app.get('/users/{user_id}')
def get_user(user_id:int) -> dict:
  user = db.select_users(user_id)
  response = {} if user==None else {'id':user[0], 'first_name':user[1], 'last_name':user[2]}
  return response

# POST /users
# Used to create a new user
@app.post("/users")
def post_user(user:User) -> dict:
  new_id = db.create_user(user.first_name, user.last_name)
  return get_user(new_id)

# PUT /users/{user_id}
@app.put('/users/{user_id}')
def put_user(user_id:int, user:User) -> dict:
  return {'success': db.update_user(user_id, user.first_name, user.last_name)}

# DELETE /users/{user_id}
@app.delete('/users/{user_id}')
def delete_user(user_id:int) -> dict:
  return {'success': db.delete_user(user_id)}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If running the server directly from Python as a module
if __name__ == "__main__":
  uvicorn.run("main-pydantic:app", host="127.0.0.1", port=8000, reload=True)