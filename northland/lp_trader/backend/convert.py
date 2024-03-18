from ..models import *
from .endpoints import *

def calculate_isk_per_lp(corp_id: int):
    corp = Corp.objects.filter(corp_id=corp_id)[0]
    print(corp.offers)


class LPConverter():
    """
    Module to perform an ISK/LP conversion from CONCORD LP into the various factions' LP.

    Conversion rates:
    Empire factions (including Ammatar Mandate and Khanid Kingdom): 1:0.8
    Non-pirate corporations that are not part of the empire: 1:0.4
    Corporations involved with factional warfare, Triglavian Invasion or any of the pirate factions: No conversion rate

    Functions:

    """
    def __init__(self, char: Character):
        self.concord_lp = char.loyalty_points["CONCORD"]
        self.EMPIRE_CONVRATE = 0.8
        self.NON_EMPIRE_CONVRATE = 0.4
    
    def get_most_profitable_items(self, region: str = "hs"):