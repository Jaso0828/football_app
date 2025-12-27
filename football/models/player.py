from django.db import models
from .club import Club


# Choices za pozicije
POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('DF', 'Defender'),
    ('MF', 'Midfielder'),
    ('FW', 'Forward'),
]


class Player(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            help_text='Ime igraca')
    birth_date = models.DateField(null=False,
                           blank=False,
                           help_text='Datum rodjenja')
    position = models.CharField(max_length=2,
                                choices=POSITION_CHOICES,
                                null=False,
                                blank=False,
                                help_text='Pozicija igraca')
    club = models.ForeignKey(Club,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL,
                             related_name='players')
    picture_url = models.URLField(max_length=1000,
                                  blank=True,
                                  null=True,
                                  help_text='Url za sliku igraca')
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f'{self.name} {self.birth_date} {self.club.name if self.club else "No Club"} {self.position}'
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'