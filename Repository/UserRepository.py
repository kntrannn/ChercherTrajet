import json
from Model.User import User

def check_user_existence(username):
    """
    Checks if a user with the given username exists in the database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    with open("Database/Entity/users.json", "r") as file:
        users = json.load(file)
        for user in users:
            if user["username"] == username:
                return True
    return False

def get_all_users():
    """
    Retrieves a list of all users from the database.

    Returns:
        list: A list of User objects.
    """
    users = []
    with open("Database/Entity/users.json", "r") as file:
        data = json.load(file)
        for i in data:
            user = User(i["id"], i["username"], i["password"])
            users.append(user)
    return users

def add_user(username, password):
    """
    Adds a new user to the database.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        User: The newly created User object.
    """
    with open("Database/Entity/users.json", "r") as file:
        users = json.load(file)
        user_id = len(users) + 1
        new_user = {
            "id": user_id,
            "username": username,
            "password": password
        }
        users.append(new_user)
    with open("Database/Entity/users.json", "w") as file:
        json.dump(users, file, indent=4)
    user_obj = User(user_id, username, password)
    return user_obj

def change_password_by_id(user_id, new_password):
    """
    Changes the password of a user with the given ID.

    Args:
        user_id (int): The ID of the user.
        new_password (str): The new password.

    Returns:
        None
    """
    with open("Database/Entity/users.json", "r") as file:
        users = json.load(file)
        for user in users:
            if user["id"] == user_id:
                user["password"] = new_password
                break
    with open("Database/Entity/users.json", "w") as file:
        json.dump(users, file, indent=4)

def get_password_by_id(user_id):
    """
    Retrieves the password of a user with the given ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The password of the user.
    """
    with open("Database/Entity/users.json", "r") as file:
        users = json.load(file)
        for user in users:
            if user["id"] == user_id:
                return user["password"]
