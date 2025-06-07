# forms.py
from django import forms
from .models import Pet,AdoptionApplication
# 定义筛选表单类

class PetFilterForm(forms.Form):
    PET_TYPE_CHOICES = Pet.PET_TYPE_CHOICES
    CAT_SUBTYPE_CHOICES = Pet.CAT_SUBTYPE_CHOICES
    DOG_SUBTYPE_CHOICES = Pet.DOG_SUBTYPE_CHOICES
    CITY_CHOICES = Pet.CITY_CHOICES
    HEALTH_STATUS_CHOICES = Pet.HEALTH_STATUS_CHOICES
    COLOR_CHOICES = Pet.COLOR_CHOICES
    SIZE_CHOICES = Pet.SIZE_CHOICES

    pet_type = forms.ChoiceField(choices=PET_TYPE_CHOICES, required=False)
    sub_type = forms.ChoiceField(choices=[], required=False)
    city = forms.ChoiceField(choices=CITY_CHOICES, required=False)
    health_status = forms.ChoiceField(choices=HEALTH_STATUS_CHOICES, required=False)
    is_stray = forms.BooleanField(required=False)
    age_min = forms.IntegerField(required=False)
    age_max = forms.IntegerField(required=False)
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False)
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        pet_type = kwargs.pop('pet_type', None)
        super(PetFilterForm, self).__init__(*args, **kwargs)
        if pet_type == 'cat':
            self.fields['sub_type'].choices = Pet.CAT_SUBTYPE_CHOICES
        elif pet_type == 'dog':
            self.fields['sub_type'].choices = Pet.DOG_SUBTYPE_CHOICES
        else:
            self.fields['sub_type'].choices = []

class PetCardForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'sub_type', 'city', 'health_status', 'is_stray', 'age', 'color', 'size', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'name': '宠物姓名',
            'pet_type': '种类',
            'sub_type': '详细种类',
            'city': '所在城市',
            'health_status': '健康状况',
            'is_stray': '是否流浪',
            'age': '年龄',
            'color': '颜色',
            'size': '体型',
            'description': '描述',
            'image': '上传图片',
        }

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ['reason']  # 申请理由
        widgets = {
            'reason': forms.Textarea(attrs={'placeholder': '请输入申请理由'}),
        }