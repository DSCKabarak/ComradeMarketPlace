import string
import secrets
from django.db.models import Model


def token_generator_and_check_if_exists(
    model: Model, length: int = 25
):
    """
    Generates a unique, secure token of the specified length.

    Args:
        model (Model): The model to check if token exists
        field_name (str): Name of the filed to check against if token exists
        length (int): The desired length of the token (default is 25).

    Returns:
        str: The generated token.
    """

    characters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(characters) for i in range(length))

    while model.objects.filter(token=token).exists():
        token = "".join(secrets.choice(characters) for i in range(length))
    return token
