from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Goods,GoodsCategory
def index(request):
    if request.method=='GET':
        #获取所有商品的分类
        category_types=GoodsCategory.CATEGORY_TYPE
        #获取商品，按照id降序排列
        goods=Goods.objects.all().order_by('-id')
        #循环商品分类,并组装结果
        data_all={}
        for type in category_types:
            data=[]
            count=0
            for good in goods:
                #count大于5，不再添加数据
                if count<4:
                    if type[0]==good.category.category_type:
                        data.append(good)
                        count+=1
            data_all['goods_'+str(type[0])]=data
        return render(request,'index.html',{'data_all':data_all,'category_types':category_types})

def list(request,goods_category,px,xh):
    if request.method=='GET':

        # 获取商品分类
        category_types=GoodsCategory.CATEGORY_TYPE
        for category_type in category_types:
            category_type=category_type[0]

        # 从model中拿到商品分类与goods_category参数匹配的商品,并按商品id逆序排列
        # 默认查询方式，按id倒叙查看
        if px=='1':
            goods=Goods.objects.filter(category_id=int(goods_category)).order_by('-id')

        elif px=='2':
            goods = Goods.objects.filter(category_id=int(goods_category)).order_by('-shop_price')
        elif px=='3':
            goods = Goods.objects.filter(category_id=int(goods_category)).order_by('shop_price')

        # 实例化一个分页对象,安装10条数据分页
        paginator=Paginator(goods,3)
        # 获取某一页的3个对象信息
        page=paginator.page(int(xh))
        print(page.paginator)


        return render(request,'list.html',{'page':page,'goods':goods})




