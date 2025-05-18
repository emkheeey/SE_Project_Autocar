from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    # Add any additional fields you want to associate with a user

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    
    # New fields for filtering
    body_type = models.CharField(max_length=50, choices=[
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('MPV', 'MPV'),
        ('Van', 'Van'),
        ('Station Wagon', 'Station Wagon'),
    ])
    transmission = models.CharField(max_length=50, choices=[
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ])

class FavoriteCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car_id = models.CharField(max_length=100)  # Store the car ID from Supabase
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'car_id')  # Prevent duplicate favorites
        
    def __str__(self):
        return f"{self.user.username}'s favorite: {self.car_id}"