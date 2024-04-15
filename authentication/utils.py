import uuid


def generate_user_id():
    """
    Uses uuid.uuid4 to generate a user id.
    """

    user_id = str(uuid.uuid4()).split('-')
    print(user_id)

    return ''.join(user_id)
