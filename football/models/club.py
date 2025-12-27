from django.utils.text import slugify
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=150,
                            unique=True,
                            null=False,
                            blank=False,
                            help_text='Naziv kluba')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            null=True,
                            blank=True,
                            help_text='Skraceno ime')
    country = models.CharField(max_length=150,
                            null=False,
                            blank=False,
                            help_text='Drzava kluba')
    city = models.CharField(max_length=150,
                            null=False,
                            blank=False,
                            help_text='grad kluba')
    league = models.CharField(max_length=150,
                            null=False,
                            blank=False,
                            help_text='liga kluba')
    founding_year = models.PositiveIntegerField(null=True,
                                     blank=True,
                                     help_text='Godina osnutka kluba')
    stadium = models.CharField(max_length=50,
                               null=True,
                               blank=True,
                               help_text='Ime stadiona')
    logo_url = models.URLField(max_length=1000,
                                null=True,
                                blank=True,
                                help_text='Url za sliku grba')
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['name']
        
    
    def __str__(self):
        return f"{self.name} {self.country} {self.league}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def year_validation(self):
        if self.founding_year and (self.founding_year < 1800 or self.founding_year > datetime.now().year):
            raise ValidationError('Godina osnutka nije validna')