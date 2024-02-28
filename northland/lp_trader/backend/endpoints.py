from esi.clients import EsiClientProvider
from esi.models import Token

from .auth import get_valid_token

esi = EsiClientProvider(app_info_text="lp-trader v0.0")


def post_names_to_ids(names: list[str]) -> dict:
    """
    Converts a list of names to IDs. Highly recommended to separate calls for names in different categories, to avoid unnecessary clutter 
    in output caused by character names or tickers

    e.g.
    character_ids = post_names_to_ids(["CCP Alpha", ["not a CCP"]])
    item_ids = post_names_to_ids(["PLEX", "Large Skill Injector"])
    alliance_ids = post_names_to_ids(["Ivy League"])

    Args:
        names (list): A list of names to be converted to IDs

    Returns:
        A dictionary of converted IDs sorted according to different categories
    """
    op = esi.client.Universe.post_universe_ids(
        names=names
    ).results()
    # print(f"Operation results - get_character_id(): {op}")
    print(op)
    results = {key: value for key, value in op.items() if value is not None}
    return results

def post_ids_to_names(ids: list[int] | int) -> dict:
    """
    Converts a list of IDs to names. Highly recommended to separate calls for names in different categories, to avoid unnecessary clutter 
    in output caused by character names or tickers

    e.g.
    character_ids = post_names_to_ids(["CCP Alpha", ["not a CCP"]])
    item_ids = post_names_to_ids(["PLEX", "Large Skill Injector"])
    alliance_ids = post_names_to_ids(["Ivy League"])

    Args:
        names (list): A list of IDs to be converted to names

    Returns:
        A dictionary of converted names sorted according to different categories
    """
    if type(ids) == int:
        ids = [ids]
    op = esi.client.Universe.post_universe_names(
        ids=ids
    ).results()
    return op

def get_loyalty_points(token: Token, raw: bool = True) -> dict:
    """
    Returns the type and quantity of loyalty points (LP) that the character owns

    Args:
        token (Token): A valid access token to access the character's data
        raw (bool): If True, returns the raw JSON data from the response. Otherwise, reformats JSON 
            to use corporation names for keys
    
    Returns:
        A dictionary of LP type (in ID/text form) and quantity
    """
    character_id = token.character_id
    op = esi.client.Loyalty.get_characters_character_id_loyalty_points(
        character_id=character_id,
        token=token.valid_access_token()
    ).results()
    if not raw:
        new = {}
        # Reparse the JSON keys to names
        for entry in op:
            lp_type, lp_quantity = entry.values()
            corp_name = post_ids_to_names(lp_type)[0]["name"]
            new[corp_name] = lp_quantity
        return new
    return op
