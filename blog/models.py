from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse

# Create your models here.

class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:200]

    class Meta:
        ordering = ["-date_posted"]


    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})        # or use args = [str(self.id)]



class Comments(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.comment