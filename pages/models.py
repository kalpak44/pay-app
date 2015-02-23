from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=200)
    isPublished = models.BooleanField(default=True)
    body = models.TextField()

    def __str__(self):
    	return self.title