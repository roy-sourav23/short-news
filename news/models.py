from django.db import models


class Article(models.Model):
    heading = models.CharField(max_length=100)
    time = models.CharField(max_length=50)
    image_url = models.URLField(blank=True)
    tags = models.TextField(blank=True)
    article = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.heading
