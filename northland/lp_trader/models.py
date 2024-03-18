from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Corp(models.Model):
    """
    Django model for Corporation object. Toggle is_npc_corp option in code or Django admin
    page to differentiate
    """
    corp_name = models.CharField(max_length=300)
    corp_id = models.IntegerField()

    is_npc_corp = models.BooleanField(default=True)
    offers = models.JSONField()

    def __str__(self):
        return self.corp_name
    

class Character(models.Model):
    """
    Django model for Character object
    """
    char_name = models.CharField(max_length=300)
    char_id = models.IntegerField()
    wallet = models.JSONField()
    loyalty_points = models.JSONField()

    last_updated = models.DateTimeField("Last Updated")
    pull_data = models.BooleanField(default=True)

    def was_recently_updated(self) -> bool:
        """
        Checks if the model has been updated within the last hour
        
        Args:
            None
        
        Returns:
            bool: Model has been updated within the last hour
        """
        now = timezone.now()
        return now - datetime.timedelta(hours=1) <= self.last_updated <= now
    
    def __str__(self):
        return self.char_name
    
class Item(models.Model):
    """
    Django model for Item object
    """
    item_name = models.CharField(max_length=300)
    item_id = models.IntegerField()
    # JSON will contain Jita buy, split and sell values of item
    # e.g. 
    # plex = Item(item_name="PLEX", item_id="44992", market_price={"buy": 4500000, "split": 4750000, "sell": 5000000})
    market_price = models.JSONField() 

    last_updated = models.DateTimeField("Last Updated")
    pull_data = models.BooleanField(default=True)

    def was_recently_updated(self) -> bool:
        """
        Checks if the model has been updated within the last hour
        
        Args:
            None
        
        Returns:
            bool: Model has been updated within the last hour
        """
        now = timezone.now()
        return now - datetime.timedelta(hours=1) <= self.last_updated <= now
    
    def __str__(self):
        return self.item_name