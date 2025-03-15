from django.conf import settings
from decimal import Decimal
from shop.models import 商品列表


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, update_quantity=False):
        '''
         * product: 表示购物车中添加或更新的product实例
         * quantity: 表示商品数量，作为可选的整数值，其默认值为1
         * update_quantity: 定义一个bool值，其表示当前数量是否需要利用给的那个的量值进行更新(true);或者新量值是否需要加入现有的量值当中(false)
       '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        创建一个迭代器再当前的类中，并返回实例对象
        """
        product_ids = self.cart.keys()
        # 获取商品信息并将其加载到购物车中
        products = 商品列表.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # 计算对象的长度
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''
        计算总价格
        '''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        '''
        清空购物车
        '''
        del self.session[settings.CART_SESSION_ID]
        self.save()
