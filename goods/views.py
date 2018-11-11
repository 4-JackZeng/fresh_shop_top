from django.shortcuts import render

from goods.models import Goods


def goods_detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})
