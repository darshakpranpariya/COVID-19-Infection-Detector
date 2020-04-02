from django.db import models

class IM(models.Model): 
    Img = models.ImageField(upload_to='images/') 
