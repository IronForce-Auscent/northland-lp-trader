from ..models import *
from .data import *
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
    
    def calculate_isk_per_lp(self, corp: Corp, _force_update: bool = False):
        """
        Calculate the ISK/lp cost efficiency of the LP store offers of a corp

        Args:
            corp (Corp): The corp to calculate LP offers for
            _force_update (bool): Force the SDE price update regardless of last_updated status (only for dev use)

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
                except IndexError as ie:
                    # Item probably doesnt exist (i.e. blueprints) due to SDE filtering
                    print(f"Item ID {type_id} skipped as item is not found in DB")
                    return 0
                except Exception as e:
                    # Some other exception that we didnt catch
                    print(f"Input cost calculation exception: {e}")
                    raise e
            return final_cost

        def _get_received_item_profits(received_items: dict) -> int:
            quantity, type_id = list(map(int, received_items.values()))
            try:
                item = Item.objects.filter(item_id=type_id)[0]
                item_sell_price = item.market_price["sell"]
                return quantity * int(item_sell_price)
            except IndexError as ie:
                # Item probably doesnt exist (i.e. blueprints) due to SDE filtering
                print(f"Item ID {type_id} skipped as item is not found in DB")
                return 0
            except Exception as e:
                # Some other exception that we didnt catch
                print(f"Profit cost calculation exception: {e}")
                raise e
            
        def _reparse_output(data: dict) -> list[dict]:
            sorted_dict = dict(sorted(data.items(), key=lambda x:x[1], reverse=True))
            return [dict([(key, value)]) for key, value in sorted_dict.items()]
            
        if _force_update or check_for_item_update():
            update_sde_prices()

        offers = corp.offers
        calculated_offers = {}
        for id, details in offers.items():
            if details["lp_cost"] == 0:
                """
                Certain LP store offers have an LP cost of 0, which will break the code (e.g. SOE token-for-ship exchanges)
                They also wont be of much use for the calculator since we cannot exchange CONCORD LP for them
                So we just set their default exchange rate to -1 to sort them to the end of the list
                """
                calculated_offers[id] = -1
                continue

            input_costs = _get_input_cost(details["required_items"])
            profits = _get_received_item_profits(details["received_items"])
            total_costs = input_costs + int(details["isk_cost"])
            isk_per_lp_rate = (profits - total_costs) / (details["lp_cost"]/ corp.lp_exchange_rate)
            calculated_offers[id] = isk_per_lp_rate
        return _reparse_output(calculated_offers)
    
    def get_profitable_trades(self):
        corps = Corp.objects.all()
        collated_exchange_rates = []
        for corp in corps:
            print(corp)
            res = self.calculate_isk_per_lp(corp)[:10]
            collated_exchange_rates.extend(res)
        return collated_exchange_rates


    

def main(corp_id):
    char = Character.objects.filter(char_name="Omalie Arnoux")[0]
    corp = Corp.objects.filter(corp_id=corp_id)[0]
    converter = LPConverter(char)
    res = converter.calculate_isk_per_lp(corp)
    print(res)

    res = converter.get_profitable_trades()
    print(res)