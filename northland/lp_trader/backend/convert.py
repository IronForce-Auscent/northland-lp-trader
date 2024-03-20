from ..models import *
from .endpoints import *


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
    
    def calculate_isk_per_lp(self, corp: Corp):
        """
        Calculate the ISK/lp cost efficiency of the LP store offers of a corp

        Args:
            corp (Corp): The corp to calculate LP offers for

        Returns:
            dict response

            Sample dict response:

        """
        def _get_input_cost(required_inputs: list[dict]) -> int:
            final_cost = 0
            for input_item in required_inputs:
                quantity, type_id = list(map(int, input_item.values()))
                try:
                    item = Item.objects.filter(item_id=type_id)[0]
                    item_sell_price = item.market_price["sell"]
                    final_cost += quantity * int(item_sell_price)
                except Exception as e:
                    print(f"Exception raised: {e}")
            return final_cost

        def _get_received_item_profits(received_items: dict) -> int:
            quantity, type_id = list(map(int, received_items.values()))
            try:
                item = Item.objects.filter(item_id=type_id)[0]
                item_sell_price = item.market_price["sell"]
                return quantity * int(item_sell_price)
            except Exception as e:
                print(f"Exception raised: {e}")
                return 0
            
        offers = corp.offers
        calculated_offers = {}
        for id, details in offers.items():
            input_costs = _get_input_cost(details["required_items"])
            profits = _get_received_item_profits(details["received_items"])
            total_costs = input_costs + int(details["isk_cost"])
            isk_per_lp_rate = (profits - total_costs) / (details["lp_cost"] / corp.lp_exchange_rate)
            calculated_offers[id] = isk_per_lp_rate
        return dict(sorted(calculated_offers.items(), key=lambda x: x[1], reverse=True))
    

def main(corp_id):
    char = Character.objects.filter(char_name="Omalie Arnoux")[0]
    corp = Corp.objects.filter(corp_id=corp_id)[0]
    converter = LPConverter(char)
    res = converter.calculate_isk_per_lp(corp)
    print(res)