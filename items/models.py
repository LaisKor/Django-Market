from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="이름")
    price = models.DecimalField(verbose_name="가격", decimal_places=0, max_digits=20)
    description = models.TextField(verbose_name="설명")
    image = models.ImageField(upload_to='static/images', verbose_name="이미지")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_items'
    )
    def __str__(self):
        return self.name

@receiver(post_delete, sender=Item)
def delete_attached_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
