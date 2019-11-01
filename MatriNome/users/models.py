from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(18)])
    gender = models.CharField(max_length=10,
                              choices=[('Male', 'Male'),
                                       ('Female', 'Female'),
                                       ('Others', 'Others'), ])
    about = models.CharField(max_length=100, default='Tell People About Yourself')
    religion = models.CharField(max_length=10,
                                choices=[('Hindu', 'Hindu'),
                                         ('Christian', 'Christian'),
                                         ('Muslim', 'Muslim'),
                                         ('Others', 'Others'),
                                         ('None', 'None'), ])
    mother_tongue = models.CharField(max_length=10,
                                     choices=[('Hindi', 'Hindi'),
                                              ('English', 'English'),
                                              ('Japanese', 'Japanese'),
                                              ('Others', 'Others'), ])

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)


class ContactRequest(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')

    def __str__(self):
        return 'ContactRequest: ' + self.user_from.username + ' - ' + self.user_to.username
