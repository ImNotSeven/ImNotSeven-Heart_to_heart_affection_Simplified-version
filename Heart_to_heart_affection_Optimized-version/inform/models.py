from django.db import models
from django.contrib.auth.models import User

from user.models import user_extend


# Create your models here.
class Pet(models.Model):
    
    PET_TYPE_CHOICES = [
        ('cat', '猫'),
        ('dog', '狗'),
    ]

    # 猫的子分类选择项
    CAT_SUBTYPE_CHOICES = [
        ('Chinese_garden', '中华田园猫'),
        ('american_shorthair', '美短'),
        ('british_shorthair', '英短'),
        ('siamese', '暹罗猫'),
        ('russian_blue', '蓝猫'),
        ('maine_coon', '缅因猫'),
        ('norwegian_forest', '挪威森林猫'),
        ('scottish_fold', '折耳猫'),
        ('persian', '波斯猫'),
        ('bengal', '孟加拉猫'),
        ('snowshoe', '雪鞋猫'),
        ('british_longhair', '英国长毛猫'),
        ('american_shorthair_tabby', '美短狸花猫'),
    ]

    # 狗的子分类选择项
    DOG_SUBTYPE_CHOICES = [
        ('Chinese_rural', '中华田园犬'),
        ('Chihuahua', '吉娃娃'),
        ('golden_retriever', '金毛'),
        ('labrador', '拉布拉多'),
        ('german_shepherd', '德牧'),
        ('french_bulldog', '法斗'),
        ('poodle', '贵宾犬'),
        ('husky', '哈士奇'),
        ('shiba_inu', '柴犬'),
        ('border_collie', '边牧犬'),
        ('bulldog', '斗牛犬'),
        ('dachshund', '腊肠犬'),
        ('bichon_frise', '比熊犬'),
        ('yorkshire_terrier', '约克夏犬'),
        ('schnauzer', '雪纳瑞'),
    ]
    CITY_CHOICES = [
        ('beijing', '北京'),
        ('shanghai', '上海'),
        ('guangzhou', '广州'),
        ('shenzhen', '深圳'),
        ('chengdu', '成都'),
        ('hangzhou', '杭州'),
        ('nanjing', '南京'),
        ('wuhan', '武汉'),
        ('xi_an', '西安'),
        ('chongqing', '重庆'),
        ('others','其它'),
    ]

    HEALTH_STATUS_CHOICES = [
        ('healthy', '健康'),
        ('ill', '有病'),
        ('recovering', '康复中'),
    ]

    COLOR_CHOICES = [
        ('black', '黑色'),
        ('white', '白色'),
        ('brown', '棕色'),
        ('gray', '灰色'),
        ('orange', '橙色'),
        ('spotted', '斑点'),
        ('striped', '条纹'),
    ]

    SIZE_CHOICES = [
        ('small', '小型'),
        ('medium', '中型'),
        ('large', '大型'),
    ]

    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPE_CHOICES)
    sub_type = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES)
    is_stray = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(user_extend, on_delete=models.CASCADE)
    is_adopted = models.BooleanField(default=False)  # 新增字段，用于标记是否被领养
    
    def __str__(self):
        return self.name
    
    def get_pet_type_display(self):
        return dict(self.PET_TYPE_CHOICES).get(self.pet_type, self.pet_type)
     
    def get_subtype_choices(self):
        return self.sub_type

    def get_city_display(self):
        return self.city
    
    def get_health_status_display(self):
        return self.health_status
    
    def get_color_display(self):
        return self.color
    
    def get_size_display(self):
        return self.size
    
class AdoptionApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_card = models.ForeignKey('Pet', on_delete=models.CASCADE)
    reason = models.TextField(default='默认申请理由', null=False)  # 申请理由
    contact = models.CharField(max_length=15,default='默认联系方式',null=False)  # 电话号码
    application_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 申请了 {self.pet_card.name}"