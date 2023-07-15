from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from configs.settings import STATIC_URL
from configs.settings import MEDIA_URL

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/noviaaaa.jpg')
    
    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d')
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        else:
            item['last_login'] = ''
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        return item
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    