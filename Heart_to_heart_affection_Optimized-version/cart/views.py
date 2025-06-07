import time
from django.urls import reverse

from django.shortcuts import redirect, render, get_object_or_404
from shop.models import 商品列表,商品类别表
from .models import OrderInfo,OrderGoods
def add_cart(request,商品_id):
    goods_id=str(商品_id)
    if goods_id:
        prev_url=request.META['HTTP_REFERER']
        print(prev_url)
        response=redirect(prev_url)
        goods_count=request.COOKIES.get(goods_id)
        if goods_count:
            goods_count=int(goods_count)+1
        else:
            goods_count=1
        response.set_cookie(goods_id,goods_count)

    return response

def show_cart(request):
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    cart_goods_money =0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        #当前商品小计
        cart_goods.total_money=int(goods_num)*cart_goods.价格
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
        #总价
        cart_goods_money=cart_goods_money+int(goods_num)*cart_goods.价格
    return render(request,'cart.html',{'cart_goods_list':cart_goods_list,
                                       'cart_goods_count':cart_goods_count,
                                       'cart_goods_money':cart_goods_money})

def remove_cart(request):
    goods_id =request.GET.get('id','')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response=redirect(prev_url)
        goods_count=request.COOKIES.get(goods_id,'')
        if goods_count:
            response.delete_cookie(goods_id)

    return response

def order(request):
    cart_goods_list = []
    # 购物车商品总数量
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        # 获取当前遍历到的商品对象
        cart_goods = 商品列表.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        # 当前商品小计
        cart_goods.total_money = int(goods_num) * cart_goods.价格
        # 把商品存列表
        cart_goods_list.append(cart_goods)
        # 累加所有商品
        cart_goods_count = cart_goods_count + int(goods_num)
        # 总价
        cart_goods_money = cart_goods_money + int(goods_num) * cart_goods.价格
    return render(request,'order.html',{'cart_goods_list':cart_goods_list,
                                        'cart_goods_count':cart_goods_count,
                                        'cart_goods_money':cart_goods_money})

def submit_order(request):
    addr =request.POST.get('addr','')
    man =request.POST.get('man','')
    phone =request.POST.get('phone','')
    extra =request.POST.get('extra','')
    order_info = OrderInfo()
    order_info.order_addr=addr
    order_info.order_man=man
    order_info.order_phone=phone
    order_info.order_extra=extra
    order_info.order_id=str(time.time()*1000)+str(time.process_time()*1000)
    order_info.save()
    response=redirect(f"{reverse('shop:success')}?id={order_info.order_id}")
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id是不是数字
        if not goods_id.isdigit():
            continue
        cart_goods=商品列表.objects.get(id=goods_id)
        order_goods=OrderGoods()
        order_goods.goods_info=cart_goods
        order_goods.goods_num=goods_num
        order_goods.goods_order=order_info
        order_goods.save()
        response.delete_cookie(goods_id)
    return response

def success(request):
    order_id=request.GET.get('id')
    orderinfo=OrderInfo.objects.get(order_id=order_id)
    order_goods_list=OrderGoods.objects.filter(goods_order=orderinfo)
    sum_money=0
    sum_num=0
    for goods in order_goods_list:
        goods.total_money=goods.goods_info.价格*goods.goods_num
        sum_money+=goods.total_money
        sum_num+=goods.goods_num
    return render(request,'success.html',{'orderinfo':orderinfo,
                              'order_goods_list':order_goods_list,
                              'sum_money':sum_money,
                              'sum_num':sum_num,
                })
