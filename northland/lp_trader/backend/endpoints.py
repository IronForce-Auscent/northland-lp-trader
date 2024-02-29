from esi.clients import EsiClientProvider
from esi.models import Token

esi = EsiClientProvider(app_info_text="lp-trader v0.0")

"""
Try to use these endpoint functions sparingly, as they take a while to run and can be
very slow at times
"""

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
        names = names
    ).results()
    results = {key: value for key, value in op.items() if value is not None}
    return results

def post_ids_to_names(ids: list[int] | int) -> dict:
    """
    Converts a list of IDs to names. Highly recommended to separate calls for names in different categories, to avoid unnecessary clutter 
    in output caused by character names or tickers

    Args:
        names (list): A list of IDs to be converted to names

    Returns:
        A dictionary of converted names sorted according to different categories
    """
    if type(ids) == int:
        ids = [ids]
    op = esi.client.Universe.post_universe_names(
        ids = ids
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
    def reparse_data(op):
        new = {}
        for entry in op:
            lp_type, lp_quantity = entry.values()
            corp_name = post_ids_to_names(lp_type)[0]["name"]
            new[corp_name] = lp_quantity
        return new
    
    character_id = token.character_id
    op = esi.client.Loyalty.get_characters_character_id_loyalty_points(
        character_id = character_id,
        token = token.valid_access_token()
    ).results()
    if not raw:
        op = reparse_data(op)
    return op

def get_corporation_divisions(token: Token, corp_id: int = 98750824) -> list[dict]:
    """
    Returns the division names for a corporation

    Args:
        token (Token): A valid access token to access the character's data
        corp_id (int): The corporation ID to pull data for (default is 98750824)

    Returns:
        A dictionary of wallet and hangar division names
    """
    op = esi.client.Corporation.get_corporations_corporation_id_divisions(
        corporation_id = corp_id,
        token = token.valid_access_token()
    ).results()
    return op

def get_corporation_wallet_balance(token: Token, corp_id: int = 98750824) -> dict:
    """
    Returns the wallet balances for a corporation

    Args:
        token (Token): A valid access token to access the character's data
        corp_id (int): The corporation ID to pull data for (default is 98750824)

    Returns:
        A dictionary of wallet balances in each corporation division
    """
    op = esi.client.Wallet.get_corporations_corporation_id_wallets(
        corporation_id = corp_id,
        token = token.valid_access_token()
    ).results()
    return op


def get_loyalty_store_offers(corp_id: int):
    """
    Returns the offers available in a corporation's LP store (NPC corp only)

    Args:
        corp_id (int): The (NPC) corporation to search
    
    Returns:

    """
    op = esi.client.Loyalty.get_loyalty_stores_corporation_id_offers(
        corporation_id = corp_id
    ).results()
    return op

def get_character_wallet_balance(token: Token, char_id: int):
    """
    Returns the wallet balance of a character

    Args:
        token (Token): A valid access token
        char_id (int): The character to pull wallet data for
    
    Returns:

    """
    op = esi.client.Wallet.get_characters_character_id_wallet(
        character_id = char_id,
        token = token.valid_access_token()
    ).results()
    return op