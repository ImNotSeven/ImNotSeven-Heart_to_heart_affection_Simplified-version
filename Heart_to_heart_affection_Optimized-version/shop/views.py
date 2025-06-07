from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import 商品列表, 商品类别表
from django.db.models import Q


def shop(request):
    所有类别 = 商品类别表.objects.all()
    类别与商品 = []
    for 每个类别 in 所有类别:
        类别与商品.append((每个类别, 商品列表.objects.filter(所属类别=每个类别, 已上架=True)[:5]))
    # 获取购物车所有商品
    # 购物车商品列表
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
    content = {'类别与商品': 类别与商品, '所有类别': 所有类别, 'cart_goods_list': cart_goods_list,
               'cart_goods_count': cart_goods_count}
    return render(request, 'shop.html', content)


def category(request, 每个类别_id):
    所有类别 = 商品类别表.objects.all()
    所需类别 = get_object_or_404(商品类别表, id=每个类别_id)
    类别与商品 = [(所需类别, 商品列表.objects.filter(所属类别=所需类别, 已上架=True))]
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
    content = {'类别与商品': 类别与商品, '所有类别': 所有类别,'cart_goods_list': cart_goods_list,
               'cart_goods_count': cart_goods_count}
    return render(request, 'shop.html', content)


def detail(request, 每个类别_id, 每件商品_id):
    所有类别 = 商品类别表.objects.all()
    商品 = get_object_or_404(商品列表, id=每件商品_id, 已上架=True)
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
    goods_id = request.GET.get('每件商品_id', 1)
    goods_data = 商品列表.objects.get(id=goods_id)
    content = {'商品': 商品, '所有类别': 所有类别, 'cart_goods_list': cart_goods_list,
               'cart_goods_count': cart_goods_count, 'goods_data': goods_data}

    return render(request, 'detail.html', content)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = 商品列表.objects.filter(Q(名称__icontains=q)|Q(所属类别__名称__icontains=q))
    return render(request, 'index.html', {'error_msg': error_msg,
                                          'post_list': post_list})


def search_detail(request, post_id):
    所有类别 = 商品类别表.objects.all()
    商品 = get_object_or_404(商品列表, id=post_id, 已上架=True)
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
    goods_id = request.GET.get('每件商品_id', 1)
    goods_data = 商品列表.objects.get(id=goods_id)
    content = {'商品': 商品, '所有类别': 所有类别, 'cart_goods_list': cart_goods_list,
               'cart_goods_count': cart_goods_count, 'goods_data': goods_data}

    return render(request, 'detail.html', content)

# print(所需类别)
#     current_goods=商品列表.objects.filter(所属类别=所需类别)
#     print(current_goods)
#     page_id=request.GET.get('每个类别',1)
#     paginator=Paginator(current_goods,8)
#     page_data=paginator.page(page_id)
