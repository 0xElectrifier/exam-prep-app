import uuid


def generate_id():
    """
    Uses uuid.uuid4 to generate an id.
    """

    model_id = str(uuid.uuid4()).split('-')

    return ''.join(model_id)


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj
