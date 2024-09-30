from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
def get_superuser():
    su_user = User.objects.filter(
        is_superuser=True).first()  # if you have more than 1 superuser, this get the first in list.
    if su_user:
        return su_user.id
    # raise DoesNotExist('Please add Super User')


class All_knifes(models.Model):
    category = [
        ('low_quality', 'low_quality'),
        ('medium_quality', "medium_quality"),
        ('high_quality', 'high_quality'),
        ('premium_quality', 'premium_quality')
    ]
    brand = models.CharField(max_length=30, blank=True, null=True)
    series = models.CharField(max_length=30, blank=True, null=True)
    steel = models.CharField(max_length=20, blank=True, null=True)
    carbon = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(6)], blank=True, null=True)
    CrMoV = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)], blank=True, null=True)
    angle = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(40)], blank=True, null=True)
    honing_add = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=category, default='low_quality')

    class Meta:
        ordering = ['brand']

    def __str__(self):
        if self.brand and self.steel:
            return f'Brand -{self.brand}, steel - {self.steel}'
        elif self.brand and not self.steel:
            return f'Brand -{self.brand}, category - {self.category}'
        else:
            return f'Brand -unknown, steel - {self.steel}'


class Grinding_data(models.Model):
    KJ = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    GA = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(40)])
    RW = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(130)])
    C1 = models.FloatField(default=50.0)
    C2 = models.FloatField(default=28.6)
    USH = models.FloatField()


class Honing_data(models.Model):
    KJ = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    GA = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(40)])
    honing_add = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(40)])
    RW = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(130)])
    FVB_S = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(130)])
    C3_C4 = models.FloatField(default=128.1)
    C5_C6 = models.FloatField(default=51.4)
    FVB_H = models.FloatField()


class Account_table(models.Model):
    date = models.DateField(blank=True, null=True, auto_now_add=True, )
    brand = models.CharField(max_length=30, blank=True, null=True, default='')
    series = models.CharField(max_length=30, blank=True, null=True, default='')
    steel = models.CharField(max_length=20, blank=True, null=True, default='')
    carbon = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(6)], blank=True, null=True,
                               default='')
    CrMoV = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)], blank=True, null=True,
                              default='')
    length = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500)], blank=True, null=True,
                               default='')
    width = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(60)], blank=True, null=True,
                              default='')
    grinding_angle = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(40)], blank=True, null=True,
                                       default='')
    honing_add = models.FloatField(blank=True, null=True, default='')
    comments = models.TextField(blank=True, null=True, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_superuser)

    def __str__(self):
        return f'Date - {self.date}'

