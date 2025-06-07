# inform/views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet,AdoptionApplication
from .forms import PetFilterForm,PetCardForm,AdoptionApplicationForm
from user.models import user_extend
from django.db.models import Q


def index(request):
    return render(request, 'pet_list.html')


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Pet
from .forms import PetFilterForm

def pet_list(request):
    pet_type = request.GET.get('pet_type', None)
    form = PetFilterForm(request.GET or None, pet_type=pet_type)

    # 默认查询所有未被领养的宠物
    pets = Pet.objects.filter(is_adopted=False)

    #     # 应用筛选条件
    # if form.is_valid():
    #     if form.cleaned_data.get('pet_type'):
    #         pets = pets.filter(pet_type=form.cleaned_data['pet_type'])
    #     if form.cleaned_data.get('sub_type'):
    #         pets = pets.filter(sub_type=form.cleaned_data['sub_type'])
    #     if form.cleaned_data.get('city'):
    #         pets = pets.filter(city=form.cleaned_data['city'])
    #     if form.cleaned_data.get('health_status'):
    #         pets = pets.filter(health_status=form.cleaned_data['health_status'])
    #     if form.cleaned_data.get('is_stray') is not None:
    #         pets = pets.filter(is_stray=form.cleaned_data['is_stray'])
    #     if form.cleaned_data.get('age_min'):
    #         pets = pets.filter(age__gte=form.cleaned_data['age_min'])
    #     if form.cleaned_data.get('age_max'):
    #         pets = pets.filter(age__lte=form.cleaned_data['age_max'])
    #     if form.cleaned_data.get('color'):
    #         pets = pets.filter(color=form.cleaned_data['color'])
    #     if form.cleaned_data.get('size'):
    #         pets = pets.filter(size=form.cleaned_data['size'])
    #
    #     print("筛选条件:", form.cleaned_data)
    #     print("符合条件的宠物数量:", pets.count())
    #     return render(request, 'pet_list.html', {'pets': pets, 'form': form})
    # 分页
    paginator = Paginator(pets, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    # 获取子分类选项
    selected_pet_type = form.data.get('pet_type', '')
    if selected_pet_type == 'cat':
        sub_type_choices = Pet.CAT_SUBTYPE_CHOICES
    elif selected_pet_type == 'dog':
        sub_type_choices = Pet.DOG_SUBTYPE_CHOICES
    else:
        sub_type_choices = []

    context = {
        'form': form,
        'page_obj': page_obj,
        'pet_type_choices': Pet.PET_TYPE_CHOICES,
        'sub_type_choices': sub_type_choices,
        'city_choices': Pet.CITY_CHOICES,
        'health_status_choices': Pet.HEALTH_STATUS_CHOICES,
        'color_choices': Pet.COLOR_CHOICES,
        'size_choices': Pet.SIZE_CHOICES,
    }

    return render(request, 'pet_list.html', context)

@login_required(login_url='/user/login')
def upload_pet_card(request):
    if request.method == 'POST':
        form = PetCardForm(request.POST, request.FILES)
        if form.is_valid():
            pet_card = form.save(commit=False)  # 不立即保存
            pet_card.created_by = request.user  # 设置当前用户
            # 获取当前用户的 UserExtend 实例
            UserExtend = get_object_or_404(user_extend, user=request.user)
            pet_card.phone = UserExtend  # 设置外键
            pet_card.save()  # 保存对象
            # 可以选择返回到主页或其他页面
            return redirect('pet_list')
    else:
        form = PetCardForm()
    return render(request, 'upload_pet_card.html', {'form': form})

def pet_detail(request, pet_id):
    # 获取宠物对象，如果不存在则返回404
    pet = get_object_or_404(Pet, id=pet_id)
    # 手动映射英文到中文
    city_mapping = dict(Pet.CITY_CHOICES)
    pet.city_display = city_mapping.get(pet.city, pet.city)  # 获取对应的中文

    health_mapping = dict(Pet.HEALTH_STATUS_CHOICES)
    pet.health_status_display = health_mapping.get(pet.health_status, pet.health_status)

    color_mapping = dict(Pet.COLOR_CHOICES)
    pet.color_display = color_mapping.get(pet.color, pet.color)

    size_mapping = dict(Pet.SIZE_CHOICES)
    pet.size_display = size_mapping.get(pet.size, pet.size)
    # 渲染详情模板
    return render(request, 'pet_detail.html', {'pet': pet})


def pet_apply(request, pet_id):
    # 获取指定的宠物
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        # 从表单获取用户提交的申请信息
        applicant_name = request.POST.get('applicant_name')
        applicant_address = request.POST.get('applicant_address')
        applicant_contact = request.POST.get('applicant_contact')
        reason = request.POST.get('reason')

        # 可在此处理申请的其他逻辑，比如保存申请信息
        #print(f"Applicant Name: {applicant_name}, Address: {applicant_address}, Contact: {applicant_contact}, Reason: {reason}")
        
        application = AdoptionApplication.objects.create(
            user=request.user,
            pet_card=pet,
            reason=reason,
            contact=applicant_contact,
        )

        # 将宠物状态设置为已领养
        pet.is_adopted = True
        pet.save()  # 保存宠物的更新
        
        return redirect('pet_list')  # 提交成功后重定向到宠物列表页面

    return render(request, 'pet_apply.html', {'pet': pet})

@login_required(login_url='/user/login')
def apply_for_pet(request, pet_id):
    # 获取用户想申请的宠物
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)  # 不立即保存
            application.user = request.user  # 设置当前用户
            application.pet_card = pet  # 关联申请的宠物

            # 获取当前用户的 UserExtend 实例
            user_extend_instance = get_object_or_404(user_extend, user=request.user)
            application.contact = user_extend_instance.contact  # 设置电话号码或其他字段
            
            application.save()  # 保存申请记录

            # 可选操作：可以在这里删除宠物或标记已申请
            pet.delete()

            return redirect('pet_of_mine')  # 成功后跳转到我的申请页面
    else:
        form = AdoptionApplicationForm()

    return render(request, 'apply_for_pet.html', {'form': form, 'pet': pet})


# 显示用户已领养的宠物
@login_required(login_url='/user/login')
def pet_of_mine(request):
    my_pets = AdoptionApplication.objects.filter(user=request.user).select_related('pet_card')
    return render(request, 'pet_of_mine.html', {'my_pets': my_pets})

def pet_search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'pet_index.html', {'error_msg': error_msg})
    post_list = Pet.objects.filter(Q(name__icontains=q)|Q(sub_type__icontains=q))
    return render(request, 'pet_index.html', {'error_msg': error_msg,
                                          'post_list': post_list})

def pet_search_detail(request, post_id):
    pet = get_object_or_404(Pet, id=post_id)
    content = {'pet': pet}

    return render(request, 'pet_detail.html', content)