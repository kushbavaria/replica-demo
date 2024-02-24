from django.db import models
from PIL import Image

from djangoProject import settings


def format_number(number):
    if abs(number) >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif abs(number) >= 1_000:
        return f"{number / 1_000:.1f}K"
    elif abs(number) >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    else:
        return str(number)


class Celeb(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=150)

    GENDER_OPTIONS = {
        "F": "Female",
        "M": "Male",
        "O": "Other"
    }

    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    age = models.IntegerField(default=18)
    # description data for api
    description = models.TextField(max_length=100)
    model_name = models.CharField(max_length=40)
    # website's rating based on customer reviews
    rating = models.FloatField(default=1)
    # followers for the most relevant social media platforms
    ig_followers = models.IntegerField(default=0)
    yt_subscribers = models.IntegerField(default=0)
    x_followers = models.IntegerField(default=0)
    tiktok_followers = models.IntegerField(default=0)
    fb_followers = models.IntegerField(default=0)

    profile_image = models.ImageField(upload_to='celeb_pics', default='static/img/png/default.png')

    def __str__(self):
        return self.name

    @property
    def total_followers(self):
        total = self.ig_followers + self.yt_subscribers + self.x_followers + self.tiktok_followers + self.fb_followers
        return format_number(total)


class Occupation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Celeb_occupation(models.Model):
    occupation_id = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    celeb_id = models.ForeignKey(Celeb, on_delete=models.CASCADE)
