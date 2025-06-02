from Repository.UserRepository import check_user_existence, get_all_users, add_user, change_password_by_id, get_password_by_id

def login_success(username, password):
    """
    Validates user login credentials.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        
    Returns:
        tuple: A tuple containing a boolean indicating success, the user object if successful, and a message.
    """
    if username == "" or password == "":
        return False, None, "Please type all fields"
    
    for user in get_all_users():
        if user.username == username and user.password == password:
            return True, user, ""
        
    return False, None, "Wrong username or password"

def register_user(username, password):
    """
    Registers a new user.
    
    Args:
        username (str): The desired username for the new user.
        password (str): The desired password for the new user.
        
    Returns:
        tuple: A tuple containing a boolean indicating success, the new user object if successful, and a message.
    """
    if username == "" or password == "":
        return False, None, "Please type all fields"
    
    if check_user_existence(username):
        return False, None, "This username is already taken"
    
    user = add_user(username, password)

    return True, user, ""

def change_password(user_id, new_password, password_confirmation):
    """
    Changes the password for a user.
    
    Args:
        user_id (int): The ID of the user whose password is to be changed.
        new_password (str): The new password.
        password_confirmation (str): Confirmation of the new password.
        
    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
    """
    if new_password == "" or password_confirmation == "":
        return False, "Please type all fields"
    
    if new_password != password_confirmation:
        return False, "Passwords do not match"
    
    if new_password == get_password_by_id(user_id):
        return False, "New password is the same as the old one"
    
    change_password_by_id(user_id, new_password)
    
    return True, ""
