import uuid

from prophesygg.logging import PROPHESY_ERROR_REPORTER
from prophesygg.utils import generate_payload


def generate_uuid(request):
    """Generates a UUID.

    Args:
        request (flask.Request): HTTP request object.

    Returns:
        A response containing the UUID
    """
    uuid_result = uuid.uuid4()
    result = uuid_result.hex

    return generate_payload("uuid-generator", {"uuid": result})
