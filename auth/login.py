def authenticate(
        username,
        password):

    users = {
        "admin": "admin123"
    }

    if username in users:

        return users[username] == password

    return False