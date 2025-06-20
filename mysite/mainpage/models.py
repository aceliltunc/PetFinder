from django.db import models
from django.contrib.auth.models import User
import datetime

class Pet(models.Model):
    ANIMAL_TYPES = [('Dog', 'Köpek'), ('Cat', 'Kedi'), ('Bird', 'Kuş'), ('Other', 'Diğer')]
    GENDERS = [('Male', 'Erkek'), ('Female', 'Dişi')]
    STATUS_CHOICES = [('Lost', 'Kayıp'), ('Found', 'Bulundu'), ('Returned', 'Teslim Edildi')]


    name = models.CharField(max_length=100, verbose_name="İsim")
    species = models.CharField(max_length=20, choices=ANIMAL_TYPES, verbose_name="Tür")
    breed = models.CharField(max_length=100, blank=True, verbose_name="Irk")
    age = models.PositiveIntegerField(verbose_name="Yaş")
    gender = models.CharField(max_length=10, choices=GENDERS, verbose_name="Cinsiyet")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    last_seen_location = models.CharField(max_length=255, verbose_name="Son Görülme Yeri")
    last_seen_date = models.DateField(default=datetime.date(2025, 1, 1), verbose_name="Son Görülme Tarihi")
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Resim")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Lost', verbose_name="Durum")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True, verbose_name="Bildirim Tarihi")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="Etiketler")

    def __str__(self):
        return f"{self.name} - {self.status}"

class Tag(models.Model):  # Many-to-Many Relationship
  name = models.CharField(max_length=50, unique=True)
  def __str__(self):
    return self.name

class PetSighting(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='sightings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    date_seen = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contact_method = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='sightings/', blank=True, null=True)

    def __str__(self):
        return f"{self.pet.name} - {self.location} - {self.date_seen}"

class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Mesaj")
    request_date = models.DateTimeField(auto_now_add=True, verbose_name="Talep Tarihi")

    def __str__(self):
        return f"Request by {self.user.username} for {self.pet.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Gönderen")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Alıcı")
    content = models.TextField(verbose_name="Mesaj")
    timestamp = models.DateTimeField(verbose_name="Zaman Damgası")
    is_read = models.BooleanField(default=False, verbose_name="Okundu")

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"

