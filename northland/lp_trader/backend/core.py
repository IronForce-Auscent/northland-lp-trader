from django.utils import timezone
from esi.models import Token

from ..models import CharacterWallet, LoyaltyStore
from .endpoints import *

def update_character_db(token: Token, force: bool) -> bool:
    """
    Updates a character's corrosponding database and returns True if success

    Args:
        token (Token): A valid access token
        force (bool): Update regardless of was_recently_updated status

    Returns:
        bool
    """
    try:
        char = CharacterWallet.objects.get(char_id=token.character_id)
        if not char.was_recently_updated() or force:
            # Update character data
            print(f"Updating data for {char.char_name}...")
            char.wallet = get_character_wallet_balance(token, char.char_id)
            char.loyalty_points = get_loyalty_points(token)
            char.last_updated = timezone.now()
            char.save()
            print("Character data updated!")
            print(f"Last updated: {char.last_updated}")
    except CharacterWallet.DoesNotExist as dne:
        print(f"Creating new character...")
        new_char = CharacterWallet(
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
        corp_store = LoyaltyStore.objects.get(corp_id=corp_id)
        print(corp_store)
        print(f"Updating offers for {corp_store.corp_name}...")
        corp_store.offers = get_loyalty_store_offers(corp_id)
        corp_store.save()
        print(f"Offers updated!")
    except LoyaltyStore.DoesNotExist as dne:
        print(f"Creating new loyalty store entry...")
        corp_name = post_ids_to_names(corp_id)[0]["name"]
        new_store = LoyaltyStore(
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