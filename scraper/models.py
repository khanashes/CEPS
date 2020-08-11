from django.db import models
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length=400)
    price = models.IntegerField()
    productUrl = models.URLField()
    imageUrl = models.URLField()
    site = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-title',)
    def __str__(self):
        return self.title

class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product.title
    class Meta:
        ordering = ("-added_date",)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    changeMessage = models.TextField(null=True)
    class Meta:
        ordering = ('date',)
    def __str__(self):
        return self.changeMessage
    
