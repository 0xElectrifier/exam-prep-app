import uuid


def generate_id():
    """
    Uses uuid.uuid4 to generate an id.
    """

    model_id = str(uuid.uuid4()).split('-')

    return ''.join(model_id)
