from django.contrib import admin
from .models import Product,WishList, Notification
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','imageUrl','site')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','date','changeMessage')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(WishList)