from django.contrib import admin
from .models import 商品列表,商品类别表
# Register your models here.
class 商品类别表Admin(admin.ModelAdmin):
    list_display = ['id','名称','图片']

admin.site.register(商品类别表,商品类别表Admin)

class 商品列表Admin(admin.ModelAdmin):
    list_display = ['id','名称','图片','所属类别','价格','库存','已上架','创建时间','修改时间']
    list_editable = ['名称','所属类别','价格','库存','已上架']
    list_per_page = 10

admin.site.register(商品列表,商品列表Admin)