from django.contrib import admin
from myapp import models

admin.site.register(models.AlbumModel)
admin.site.register(models.PhotoModel)
admin.site.register(models.Product)
admin.site.register(models.OrdersModel)
admin.site.register(models.DetailModel)