import os
from pathlib import Path
import mysql.connector as mysql
from dotenv import load_dotenv


class DatabaseStore:
  def __init__(self) -> None:
    """
    A database store for user data, using MySQL.
    """
    load_dotenv(Path(__file__).resolve().parent.parent / '.env', override=True)
    self.db_host = os.environ['MYSQL_HOST']
    self.db_user = os.environ['MYSQL_USER']
    self.db_pass = os.environ['MYSQL_PASSWORD']
    self.db_name = os.environ['MYSQL_DATABASE']

  def _get_connection(self):
    return mysql.connect(host=self.db_host, database=self.db_name, user=self.db_user, passwd=self.db_pass)

  def get_users(self) -> dict[int, dict[str, str]]:
    """
    Return the entire users collection as a dictionary mapping user IDs to user records.
    """
    db = self._get_connection()
    cursor = db.cursor(dictionary=True)
    query = 'select id, first_name, last_name from users;'
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()

    users = {}
    for row in result:
      # We ignore the type errors because pylance is assuming the cursor is returning tuples, but we set dictionary=True so it actually returns dictionaries
      users[row['id']] = {'first_name': row['first_name'], 'last_name': row['last_name']}  # type: ignore
    return users  # type: ignore

  def get_user(self, user_id: int) -> dict[str, str] | None:
    """
    Return the user record for the given user ID, or None if the user does not exist.
    """
    db = self._get_connection()
    cursor = db.cursor(dictionary=True)
    query = 'select id, first_name, last_name from users where id=%s;'
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    db.close()

    if result is None:
      return None
    return {'id': str(result['id']), 'first_name': result['first_name'], 'last_name': result['last_name']}  # type: ignore

  def create_user(self, first_name: str, last_name: str) -> dict[str, str]:
    """
    Create a new user with the given first and last name, assign them a new unique ID, and return the user record.
    """
    db = self._get_connection()
    cursor = db.cursor()
    cursor.execute('insert into users (first_name, last_name, created_at) values (%s, %s, NOW())', (first_name, last_name))
    db.commit()
    user_id = cursor.lastrowid
    db.close()
    return {'id': str(user_id), 'first_name': first_name, 'last_name': last_name}

  def update_user(self, user_id: int, first_name: str, last_name: str) -> bool:
    """
    Update the user record for the given user ID with the new first and last name.
    Return True if the update was successful, or False if the user does not exist.
    """
    db = self._get_connection()
    cursor = db.cursor()
    query = 'update users set first_name=%s, last_name=%s where id=%s;'
    values = (first_name, last_name, user_id)
    cursor.execute(query, values)
    db.commit()
    rowcount = cursor.rowcount
    db.close()
    return rowcount == 1

  def delete_user(self, user_id: int) -> bool:
    """
    Delete the user record for the given user ID.
    Return True if the deletion was successful, or False if the user does not exist.
    """
    db = self._get_connection()
    cursor = db.cursor()
    cursor.execute('delete from users where id=%s;', (user_id,))
    db.commit()
    rowcount = cursor.rowcount
    db.close()
    return rowcount == 1


user_store = DatabaseStore()
