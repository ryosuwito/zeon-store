from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from membership.models import Member

class Customer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #done
    seller = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_customer', null=True)
    name = models.CharField(max_length=250, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
    home_provinsi = models.CharField(max_length=250, blank=True)
    home_kota = models.CharField(max_length=250, blank=True)
    home_kecamatan = models.CharField(max_length=250, blank=True)
    home_kelurahan = models.CharField(max_length=250, blank=True)
    home_address = models.CharField(max_length=250, blank=True)
    profile_photo = models.ImageField(upload_to = 'profile_photo', blank=True)

    def get_profile_photo_url(self):
        return ("/media/%s"%self.profile_photo)

    def get_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
        
    def get_home_address(self):
        return '%s, %s, %s, %s - %s' % (self.home_address, 
            self.home_kelurahan, 
            self.home_kecamatan,
            self.home_kota,
            self.home_provinsi)
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        customer = Customer(user=instance)
        customer.save()
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.customer.save()