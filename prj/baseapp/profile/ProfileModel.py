from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    address = models.TextField(blank=True, null=True)
    iframe_code = models.CharField(max_length=500, blank=True, null=True)  # Adjust max_length as needed
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    fb = models.URLField(max_length=200, blank=True, null=True, verbose_name='Facebook')
    linkedin = models.URLField(max_length=200, blank=True, null=True, verbose_name='LinkedIn')
    insta = models.URLField(max_length=200, blank=True, null=True, verbose_name='Instagram')
    youtube = models.URLField(max_length=200, blank=True, null=True, verbose_name='YouTube')
    x = models.URLField(max_length=200, blank=True, null=True, verbose_name='X (formerly Twitter)')
    skype = models.CharField(max_length=50, blank=True, null=True)
  
    def __str__(self):
        return self.name if self.name else self.email

class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fb = models.URLField(max_length=200, blank=True, null=True, verbose_name='Facebook')
    youtube = models.URLField(max_length=200, blank=True, null=True, verbose_name='YouTube')
    x = models.URLField(max_length=200, blank=True, null=True, verbose_name='X (formerly Twitter)')
    phone_number = models.CharField(max_length=15)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='team_profile_pics/')
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"