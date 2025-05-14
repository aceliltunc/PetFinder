from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    ANIMAL_TYPES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Rabbit', 'Rabbit'),
        ('Other', 'Other'),
    ]

    GENDERS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=ANIMAL_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDERS)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pet_images/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} for {self.pet.name}"
