from django.db import models
from django.utils import timezone


class Post(models.Model):
    CITIES = (
        ('ny', 'New York'),
        ('sm', 'Santa Monica')
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    city = models.CharField(max_length=50, choices=CITIES, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.title} {self.author} {self.city}'


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postviews')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)
