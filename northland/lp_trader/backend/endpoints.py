from esi.clients import EsiClientProvider
from esi.models import Token

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
    results = {key: value for key, value in op.items() if value is not None}
    return results

def get_loyalty_points(character_id: int, token: Token) -> dict:
    """
    Returns the type and quantity of loyalty points (LP) that the character owns

    Args:
        character_id (int): The character ID to get data from
        token (Token): A valid access token to access the character's data
    
    Returns:
        A dictionary of LP type (in ID form) and quantity
    """
    op = esi.client.Loyalty.get_characters_character_id_loyalty_points(
        character_id=character_id,
        token=token.valid_access_token()
    ).results()
    # print(f"Operation results - get_loyalty_points(): {op}")
    return op