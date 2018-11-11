from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods


def add_cart(request):
    if request.method=='POST':
        # 添加session中的数据格式为：
        # 添加session中的数据格式为:key==>goods,
        # value==>[[id1,num],[id2,num]...]

        # 1.没有登录的情况
        # 1.1添加到购物车的数据，其实就是添加到session中
        # 1.2 如果商品已经加入到session中，则修改session中商品的个数
        # 1.3如果商品没有添加到session中，则添加

        # 获取从ajax中传递的商品的id和商品的个数
        goods_id=request.POST.get('goods_id')
        goods_num=request.POST.get('goods_num')
        # 组装存储的数据结构
        goods_list=[goods_id,goods_num,1]
        # 判断session中是否存储了
        if request.session.get('goods'):

            #标识符:用于判断当前加入到购物车中的商品
            # 说明购物车中已经存在了该商品，则修改flag=1，否则flag还是等于0
            flag=0
            # 说明购物车中已经存储了商品信息
            session_goods=request.session['goods']
            for goods in session_goods:
                # 循环判断，判断加入到session中商品是否已经存在于session中
                if goods_id==goods[0]:
                    goods[1]=int(goods[1])+int(goods_num)
                    # 标识符，修改到session中的商品后，标识符修改为1
                    flag=1
                #flag为0，表示添加到session中的商品之前并没有添加
            if not flag:
                session_goods.append(goods_list)
            #修改成功session中商品的信息
            request.session['goods']=session_goods
            cart_count=len(session_goods)
        else:
            # 购物车中没有存储商品信息
            data=[]
            data.append(goods_list)
            request.session['goods']=data
            cart_count=1
        return JsonResponse({'code':200,'cart_count':cart_count})
def cart(request):
    if request.method=='GET':
        # 需要判断用户是否登录， session['user_id']
        # 1. 如果登录，则购物车中展示当前登录用户的购物车表中的数据
        # 2. 如果没有登录，则购物车页面中展示session中的数据
        user_id=request.session.get('user_id')
        goods_id = request.POST.get('goods_id')
        if user_id:
            shop_cart=ShoppingCart.objects.filter(user_id=user_id)
            goods_all=[(cart.goods,cart.is_select,cart.nums) for cart in shop_cart]
            user_id = request.session.get('user_id')
            # 如果能够获取到
            # 获取购物车中的商品总数据
            carts = ShoppingCart.objects.filter(user_id=user_id)
            all_nums = 0
            for cart in carts:
                all_nums += cart.nums
            # 获取购物车中勾选的商品数据
            carts = ShoppingCart.objects.filter(user_id=user_id)
            all_num = 0
            for cart in carts:
                if cart.is_select:
                    all_num += cart.nums

            return render(request,'cart.html',{'goods_all':goods_all, 'all_nums':all_nums,'all_num':all_num})
        else:
            #             没有登录
            session_goods = request.session.get('goods')

            user_id = request.session.get('user_id')
            # 如果能够获取到
            if user_id:
                # 获取购物车中的商品总数据
                carts = ShoppingCart.objects.filter(user_id=user_id)
                all_nums = 0
                for cart in carts:
                    all_nums += cart.nums
                # 获取购物车中勾选的商品数据
                carts = ShoppingCart.objects.filter(user_id=user_id)
                all_num = 0
                for cart in carts:
                    if cart.is_select:
                        all_num += cart.nums
            #拿到session中所有的商品id值
            if session_goods:
                goods_all = [(Goods.objects.get(pk=good[0]), good[2], good[1]) for good in session_goods]
            else:
                goods_all = ''
            return render(request, 'cart.html', {'goods_all': goods_all,'all_nums':all_nums,'all_num':all_num})

def f_price(request):
    """
    返回购物车或session中商品的价格，和总价
    {key:[[id1, price1],[id2, price2]], key2: total_price}
    """
    user_id = request.session.get('user_id')
    if user_id:
        # 获取当前登录系统的用户的购物车中的数据
        carts=ShoppingCart.objects.filter(user_id=user_id)
        cart_data={}
        cart_data['goods_price']=[(cart.goods_id,cart.nums*cart.goods.shop_price)for cart in carts]
        all_price=0
        for cart in carts:
            if cart.is_select:
                all_price+=cart.nums*cart.goods.shop_price
        cart_data['all_price']=all_price
        # print(cart.nums)

    else:
        # 拿到session中所有的商品信息,[id num,is_select]
        session_goods = request.session.get('goods')
        cart_data = {}
        data_all = []
        # 计算总价
        all_price = 0
        for goods in session_goods:

            data = []
            data.append(goods[0])
            g = Goods.objects.get(pk=goods[0])
            data.append(int(goods[1]) * g.shop_price)
            data_all.append(data)
            # 判断如果商品勾选了，才计算总价格
            if goods[2]:
                all_price += int(goods[1]) * g.shop_price
        cart_data['goods_price'] = data_all
        cart_data['all_price'] = all_price
    return JsonResponse({'code': 200, 'cart_data': cart_data})

def check(request):
    if request.method=='POST':
        goods_id=request.POST.get('goods_id')
        session_goods=request.session.get('goods')
        data=[]
        if session_goods:
            # 如果没有登录，在session中取goods
            for goods in session_goods:
                if goods_id==goods[0]:
                    if goods[2]:
                        goods[2]=False
                    else:
                        goods[2]=True

                data.append(goods)
            request.session['goods'].clear()
            request.session['goods']=data
            return JsonResponse({'code':200,'goods': session_goods})
        else:
            # 登录情况下在数据库中找
            shop_cart=ShoppingCart.objects.filter(goods_id=goods_id).first()
            if shop_cart.is_select:
                shop_cart.is_select=False
            else:
                shop_cart.is_select=True
            shop_cart.save()

            return JsonResponse({'code':200,'msg':'请求成功'})





def f_nums(request):
    if request.method=='GET':
        #获取当前登录系统的用户user_id
        user_id = request.session.get('user_id')
        #如果能够获取到
        if user_id:
            #获取购物车中的数据
            carts=ShoppingCart.objects.filter(user_id=user_id)
            all_nums=0
            for cart in carts:
                if cart.is_select:
                    all_nums +=cart.nums
            return render(request, 'cart.html', {'all_nums':all_nums})
            print('=====')
            print(all_nums)


def cart_count(request):
    if request.method=='GET':
        # 获取到当前登录系统的用户
        user_id=request.session.get('user_id')
        if user_id:
            count=ShoppingCart.objects.filter(user_id=user_id).count()
            pass




