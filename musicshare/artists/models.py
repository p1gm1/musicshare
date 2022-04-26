from django.db import models

from musicshare.base import CharFieldChoiceEnum


class ArtistStatus(CharFieldChoiceEnum):
    STATUS_ACTIVE = 'active'
    STATUS_RETIRED = 'retired'


class Artist(models.Model):
    name = models.CharField(max_length=155)
    alias = models.CharField(max_length=155, unique=True)
    band = models.CharField(max_length=155, null=True)
    instrument = models.CharField(max_length=155, null=True)
    status = models.CharField(max_length=155, 
                              default=ArtistStatus.STATUS_ACTIVE.value, 
                              choices=ArtistStatus.choices())
    
    class Meta:
        db_table = 'artists'

    def __str__(self) -> str:
        return f"{self.name} from {self.band}, aka {self.alias}"
