from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username and password.
    :param username: User's username (string)
    :param password: User's un-encrypted password (string)
    :return: UserModel object if authentication was successful, else None
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT verified their authorization header is correct.
    :param payload: User id in a dictionary with 'identity' as key
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
