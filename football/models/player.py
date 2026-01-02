from django.db import models
from .club import Club

class Player(models.Model):
    name = models.CharField(max_length=150)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='players')
    age = models.PositiveIntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=50, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    photo_url = models.URLField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    height = models.CharField(max_length=10, blank=True, null=True)  
    weight = models.CharField(max_length=10, blank=True, null=True)  
    
    def __str__(self):
        return f"{self.name} - {self.club.name}"