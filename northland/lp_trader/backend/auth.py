from esi.models import Token

from .errors import AuthException


def get_valid_token(request) -> Token:
    """
    Checks for a valid token, and returns if one is found

    Args:
        None

    Returns:
        A Token-type object for ESI calls
    """
    try:
        valid_token = Token.objects.filter(
            user = request.user
        ).require_valid()
        if valid_token.exists():
            return valid_token
    except Exception as e:
        raise AuthException(f"Exception thrown: {e}")