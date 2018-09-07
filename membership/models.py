from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class PackageGroup(models.Model):
    """

    FREE_TRIAL = 0 #FreeTrial
    WEB = 1 #Web
    IOS = 2 #Ios
    ANDROID = 3 #Android
    WEB_AND_IOS_MEMBER = 4 #IosHybrid
    WEB_AND_ANDROID_MEMBER = 5 #AndroidHybrid
    ANDROID_AND_IOS_MEMBER = 6 #Mobile
    FULL_PACKAGE_MEMBER = 7 #Premium

    """
    FREE_TRIAL = 0 #FreeTrial
    WEB = 1 #Web
    IOS = 2 #Ios
    ANDROID = 3 #Android

    TYPE_CHOICES = (
        (FREE_TRIAL, 'Free Trial'),
        (WEB, 'Web'),
        (IOS, 'Ios'),
        (ANDROID, 'Android'),
    )

    name = models.CharField(db_index=True, max_length=50, blank=True) 
    code = models.PositiveSmallIntegerField(unique=True,choices=TYPE_CHOICES,default=0)

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.OneToOneField(User, related_name="user_member", on_delete=models.CASCADE)
    package_group = models.ManyToManyField(PackageGroup, blank=True, related_name="package_group")
    site = models.OneToOneField(Site, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user.username
