from django.db import models

# 商品資料庫格式
class Product(models.Model):
    # 商品id：自動遞增
    product_id = models.AutoField(primary_key=True)
    # 商品名稱：不能null 限制12字 文字
    product_name = models.CharField(max_length=12, null=False)
    # 商品描述：可以null 限制50字 文字
    product_description = models.CharField(max_length=50, null=True, blank=True)
    # 商品價格：不能null 數字
    product_price = models.IntegerField(null=False)
    # 促銷種類：可以null 數字
    product_sale = models.IntegerField(null=True, default=0)
    # 圖片連結：不能null 文字
    product_image_link = models.CharField(max_length=255, default='assets/img/')
    # 庫存量：不能null 數字
    product_storage = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.product_name
    
# class ProductModel(models.Model):
#     pname =  models.CharField(max_length=100, default='')
#     pprice = models.IntegerField(default=0)
#     pimages = models.CharField(max_length=100, default='')
#     pdescription = models.TextField(blank=True, default='')
#     def __str__(self):
#         return self.pname
        
class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    customname =  models.CharField(max_length=100, default='')
    customemail =  models.CharField(max_length=100, default='')
    customaddress =  models.CharField(max_length=100, default='')
    customphone =  models.CharField(max_length=100, default='')
    paytype =  models.CharField(max_length=50, default='')
    def __str__(self):
        return self.customname
     
class DetailModel(models.Model):
    dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)
    pname = models.CharField(max_length=100, default='')
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    def __str__(self):
        return self.pname


    
class AlbumModel(models.Model):
    adate = models.DateTimeField(auto_now=True)
    alocation = models.CharField(max_length=200, blank=True, default='')
    atitle = models.CharField(max_length=100, null=False)
    adesc = models.TextField(blank=True, default='')
    def __str__(self):
        return self.atitle

class PhotoModel(models.Model):
    palbum = models.ForeignKey('AlbumModel', on_delete=models.CASCADE)
    psubject = models.CharField(max_length=100, null=False)
    pdate = models.DateTimeField(auto_now=True)
    purl = models.CharField(max_length=100, null=False)
    phit = models.IntegerField(default=0)
    def __str__(self):
        return self.psubject
    
