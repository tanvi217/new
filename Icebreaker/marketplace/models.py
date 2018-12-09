from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class product(models.Model):
    fullname = models.ForeignKey(User, on_delete=models.PROTECT,null = True, blank = True) #foreign key from user table from django-admin
    product_title = models.CharField(max_length = 100)
    product_type = models.TextField(null=True)
    overview = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to="media", blank=True)
#    pic = models.ForeignKey(profile, on_delete=models.PROTECT,null = True, blank = True)

    def __str__(self):
        return self.product_title

    def snippept(self):
        return self.overview[:50] + "..."
