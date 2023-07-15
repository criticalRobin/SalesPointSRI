from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from configs.settings import MEDIA_URL

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(MEDIA_URL, 'img/noviaaaa.jpg')
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions'])
        item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        return item
    