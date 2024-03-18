from django.utils import timezone
from django.db import models
from esi.models import Token
from tqdm import tqdm

from ..models import *
from .endpoints import *

import numpy as np
import math
import time

def temp():
    chars = Character.objects.all()
    for char in chars:
        print(f"Checking LP list for {char}")
        lp_list = char.loyalty_points
        for store, _ in lp_list.items():
            print(f"Attempting to add/update LP store for {store}")
            store_id = post_names_to_ids([store])["corporations"][0]["id"]
            _ = update_corp_loyalty_store(store_id)
    print("All stores updated successfully")
    return False


def check_for_character_update():
    chars = Character.objects.all()
    for char in chars:
        if not char.was_recently_updated():
            token = Token.objects.filter(character_id=char.char_id)
            _ = update_character_db(token)
    return False

def update_character_db(token: Token, force: bool = False) -> bool:
    """
    Updates a character's corrosponding database

    Args:
        token (Token): A valid access token
        force (bool): Update regardless of was_recently_updated status

    Returns:
        bool
    """
    try:
        char = Character.objects.get(char_id=token.character_id)
        if not char.was_recently_updated() or force:
            # Update character data
            print(f"Updating data for {char.char_name}...")
            char.wallet = get_character_wallet_balance(token, char.char_id)
            char.loyalty_points = get_loyalty_points(token, raw=False)
            char.last_updated = timezone.now()
            char.save()
            print("Character data updated!")
            print(f"Last updated: {char.last_updated}")
    except Character.DoesNotExist as dne:
        print(f"Creating new character...")
        new_char = Character(
            char_name = token.character_name,
            char_id = token.character_id,
            wallet = get_character_wallet_balance(token, token.character_id),
            loyalty_points = get_loyalty_points(token),
            last_updated = timezone.now()
        )
        new_char.save()
        print(f"New character ({token.character_name}) created!")
    except Exception as e:
        print(f"Exception: {e}")
        return False
    return True

def update_corp_loyalty_store(corp_id: int) -> bool:
    """
    Updates a corporation's corrosponding database for loyalty store offers.
    Assumes that the loyalty store's offers have changed, and updates accordingly

    Args:
        corp_id (int): The corporation ID to update offers for
    
    Returns:
        bool
    """
    try:
        corp_store = Corp.objects.get(corp_id=corp_id)
        print(f"Updating offers for {corp_store.corp_name}...")
        corp_store.offers = get_loyalty_store_offers(corp_id)
        corp_store.save()
        print(f"Offers updated!")
    except Corp.DoesNotExist as dne:
        print(f"Creating new loyalty store entry...")
        corp_name = post_ids_to_names(corp_id)[0]["name"]
        new_store = Corp(
            corp_name = corp_name, 
            corp_id = corp_id, 
            offers = get_loyalty_store_offers(corp_id)
        )
        new_store.save()
        print(f"New entry for corp {corp_name} created!")
    except Exception as e:
        print(f"Exception {e}")
        return False
    return True


def update_sde() -> bool:
    """
    Update the static database using the Fuzzworks' SDE library.
    Price data should not be populated together with the SDE as it will take quite a long time
    using the get_item_prices() endpoint function

    Args:
        None

    Returns:
        bool
    """
    try:
        print("Clearing current database...")
        Item.objects.all().delete() # Try to delete all the items in the Item model
        print("Database cleared!")
    except Exception as e:
        # Do nothing
        pass

    data = get_static_data()
    print("New data obtained, updating database with new data...")

    try:
        for entry in tqdm(data):
            new_item = Item(
                item_name = entry["typeName"],
                item_id = entry["typeID"],
                market_price = {},
                last_updated = timezone.now()
            )
            new_item.save()
        print("All items updated!")
    except Exception as e:
        print(f"Exception thrown: {e}")
        raise e
    update_sde_prices()
    return True


def update_sde_prices() -> bool:
    """
    Update the internal pricings for items using the get_item_prices endpoint.
    Max. 5000 items per request
    """

    request_inputs = []
    items = Item.objects.all()
    queryset_len = len(items)
    request_inputs = np.array_split(items, math.ceil(queryset_len / 2500))
    for item_list in request_inputs:
        item_inputs = [n.item_id for n in item_list]
        print("Querying for data... ")
        start = time.time()
        _, res = get_item_prices(item_inputs)
        end = time.time()
        print(f"Data queried successfully! (runtime: {end - start})")
    return res