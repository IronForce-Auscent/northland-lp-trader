from django.conf import settings
from esi.clients import EsiClientProvider
from esi.models import Token
from typing import *

import pandas as pd
import requests

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
        A tuple containing key-value pairs of the hangar and wallet divisions


    """
    op = esi.client.Corporation.get_corporations_corporation_id_divisions(
        corporation_id = corp_id,
        token = token.valid_access_token()
    ).results()
    hangar, wallet = op["hangar"], op["wallet"]
    return hangar, wallet

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


def get_loyalty_store_offers(corp_id: int) -> dict:
    """
    Returns the offers available in a corporation's LP store (NPC corp only)

    Args:
        corp_id (int): The (NPC) corporation to search
    
    Returns:
        dict

        Sample dict response:
        {
            "4767": {
                "isk_cost": 25200000, 
                "lp_cost": 37800, 
                "required_items": 
                    [
                        {
                        "quantity": 1, 
                        "type_id": 14297
                        },
                        ...
                    ], 
                "received_items": 
                    {
                        "quantity": 1,
                        "type_id": 28803
                    }
                },
                ...
        }
    """
    op = esi.client.Loyalty.get_loyalty_stores_corporation_id_offers(
        corporation_id = corp_id
    ).results()
    res = {}
    for offer in op:
        res[offer["offer_id"]] = {
            "isk_cost": offer["isk_cost"],
            "lp_cost": offer["lp_cost"],
            "required_items": offer["required_items"],
            "received_items": {
                "quantity": offer["quantity"],
                "type_id": offer["type_id"]
            }
        }
    return res

def get_character_wallet_balance(token: Token, char_id: int) -> dict:
    """
    Returns the wallet balance of a character

    Args:
        token (Token): A valid access token
        char_id (int): The character to pull wallet data for
    
    Returns:
        dict
    """
    op = esi.client.Wallet.get_characters_character_id_wallet(
        character_id = char_id,
        token = token.valid_access_token()
    ).results()
    return op


def get_static_data() -> list[dict]:
    """
    Returns the latest static data from Fuzzworks

    Args:
        None
    
    Returns:
        A list object
    """
    data = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/invTypes.csv")
    data.drop(data[data["published"] == False].index, inplace=True)
    #data = data[data["typeName"].str.contains("SKIN") == False]
    to_exclude = ["description","mass","volume","capacity","portionSize","raceID","basePrice","published","marketGroupID","iconID","soundID","graphicID"]
    data.drop(labels=to_exclude, inplace=True, axis=1)
    return data.to_dict(orient="records")

def get_blueprint_static_data() -> list[dict]:
    """
    Returns the latest blueprint data from Fuzzworks

    Args:
        None

    Returns:
        A list object
    """
    data = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/industryActivityMaterials.csv")
    data.drop(data[data["activityID"] != 1].index, inplace=True)
    return data.to_dict(orient="records")

def get_blueprint_build_cost(bp_ids: int | list[int]):
    """
    Returns the build cost of a blueprint/list of blueprints using the Evecookbook API

    Args:
        int | list[int]: Type IDs of the blueprints to calculate build costs for. Max 20 type IDs per request
    
    Returns:

    """
    if type(bp_ids) == int:
        bp_ids = list(bp_ids)
    
    target = "https://evecookbook.com/api/buildCost"
    params = {
        "blueprintTypeId": ",".join(list(map(str, bp_ids))),
        "quantity": 1,
        "priceMode": "sell",
        "additionalCosts": 0,
        "baseMe": 0,
        "componentsMe": 0,
        "system": "Jita",
        "facilityTax": 0,
        "industryStructureType": "Station"
    }
    req = requests.get(target, params=params)
    statcode, body = req.status_code, req.json()
    return statcode, body


def get_item_prices(typeIds: list[int] = [44992], regionId: int = 30000142) -> Tuple[int, list]:
    """
    Returns the latest price data for an item from Janice appraisal API. Searches
    for price data in Jita 4-4

    Args:
        typeNames (list): A list of item names to look up prices for. Defaults to ["PLEX"]

    Returns:
        A tuple object containing a status code and JSON response

        Sample JSON response:
        {
            '44992': {
                'buy': 4883000.0,
                'split': 4961000.0,
                'sell': 5039000.0
            },
            ...
        }
    """
    typeIds_parsed = typeIds if len(typeIds) == 1 else ",".join(list(map(str, typeIds)))
    target = "https://market.fuzzwork.co.uk/aggregates/"
    params = {
        'region': regionId,
        'types': typeIds_parsed
    }
    req = requests.get(target, params=params)
    statcode, body = req.status_code, req.json()
    res = {}
    for key, value in body.items():
        buy, sell = float(value["buy"]["max"]), float(value["sell"]["min"])
        split = (buy + sell) / 2
        new_item = {
            "buy": buy,
            "split": split,
            "sell": sell
        }
        res[key] = new_item
    return statcode, res