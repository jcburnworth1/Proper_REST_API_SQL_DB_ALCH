## File will help with proper authentication
## Import libraries
from resources.user import UserModel
from werkzeug.security import safe_str_cmp  ## Safe string comparison

## Authenticate Function
def authenticate(username, password) -> UserModel:
    """
    Simple method to find user data rather than looping
    :param username: The user's login
    :param password: The user's password
    :return: UserModel object if found, None if not found
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload) -> UserModel:
    """
    Simple method to find user data rather than looping
    :param payload:
    :return: user object if found, None if not found
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
