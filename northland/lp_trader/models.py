from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class LoyaltyStore(models.Model):
    corp_name = models.CharField(max_length=300)
    corp_id = models.IntegerField()
    offers = models.JSONField()

    def __str__(self):
        return self.corp_name
    

class CharacterWallet(models.Model):
    char_name = models.CharField(max_length=300)
    char_id = models.IntegerField()
    wallet = models.JSONField()
    loyalty_points = models.JSONField()

    last_updated = models.DateTimeField("Last Updated")
    pull_data = models.BooleanField(default=False)

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