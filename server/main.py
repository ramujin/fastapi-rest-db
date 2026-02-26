# Necessary Imports
from pathlib import Path
from fastapi import FastAPI, Request  # The main FastAPI import and Request object
from fastapi.responses import HTMLResponse  # Used for returning HTML responses (JSON is default)
from fastapi.staticfiles import StaticFiles  # Used for making static resources available to server
from fastapi.templating import Jinja2Templates  # Used for generating HTML from templatized files
from pydantic import BaseModel  # Used to define request models
import uvicorn  # Used for running the app directly through Python

# Local Imports
import store  # The "database" store for our users


# Configuration
app = FastAPI()  # Specify the "app" that will run the routing

base_dir = Path(__file__).resolve().parent
views = Jinja2Templates(directory=str(base_dir / 'views'))  # Specify where the HTML files are located
static_files = StaticFiles(directory=str(base_dir / 'public'))  # Specify where the static files are located
app.mount('/public', static_files, name='public')  # Mount the static files directory to /public


# Define a User class that matches the SQL schema we defined for our users
class User(BaseModel):
  first_name: str
  last_name: str


# Home route to load the main page in a templatized fashion
# GET /
@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request) -> HTMLResponse:
  """
  1. Query the database for all users
  2. Format the results as a list of tuples (user_id, first_name, last_name)
  3. Return the index.html template with the users list as context
  """
  users = store.user_store.get_users()
  users_list = [(user_id, user['first_name'], user['last_name']) for user_id, user in sorted(users.items())]

  return views.TemplateResponse('index.html', {'request': request, 'users': users_list})


# RESTful User Routes
# GET /users
# Used to query a collection of all users
@app.get('/users')
async def get_users() -> dict[str, list[dict[str, str]]]:
  """
  1. Query the database for all users
  2. Format the results as a list of dictionaries (JSON objects!) where the dictionary keys are:
    'id', 'first_name', and 'last_name'
  3. Return this collection as a JSON object, where the key is 'users' and the value is the list
  """

  users = store.user_store.get_users()
  return {'users': [{'id': str(user_id), 'first_name': user['first_name'], 'last_name': user['last_name']} for user_id, user in sorted(users.items())]}


# GET /users/{user_id}
# Used to query a single user
@app.get('/users/{user_id}')
async def get_user(user_id: int) -> dict[str, str]:
  """
  1. Query the database for the user with a database ID of 'user_id'
  2. If the user does not exist, return an empty object
  3. Otherwise, format the result as JSON where the keys are: 'id', 'first_name', and 'last_name'
  """

  user = store.user_store.get_user(user_id)
  return {} if user is None else user


# POST /users
# Used to create a new user
@app.post('/users')
async def post_user(user: User) -> dict[str, str]:
  """
  1. Retrieve the data asynchronously from the 'request' object (Pydantic automatically hydrates the user object for us)
  2. Extract the first and last name from the POST body
  3. Create a new user in the database
  4. Return the user record back to the client as JSON
  """

  return store.user_store.create_user(user.first_name, user.last_name)


# PUT /users/{user_id}
@app.put('/users/{user_id}')
async def put_user(user_id: int, user: User) -> dict[str, bool]:
  """
  1. Retrieve the data asynchronously from the 'request' object (Pydantic automatically hydrates the user object for us)
  2. Attempt to update the user first and last name in the database
  3. Return the update status under the 'success' key
  """

  return {'success': store.user_store.update_user(user_id, user.first_name, user.last_name)}


# DELETE /users/{user_id}
@app.delete('/users/{user_id}')
async def delete_user(user_id: int) -> dict[str, bool]:
  """
  1. Attempt to delete the user from the database
  2. Return the delete status under the 'success' key
  """

  return {'success': store.user_store.delete_user(user_id)}


# If running the server directly from Python as a module
if __name__ == '__main__':
  uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, workers=1)
