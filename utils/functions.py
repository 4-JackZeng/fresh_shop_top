import random
from datetime import datetime
def get_order_sn():
    """生成随机的订单号"""
    sn=''
    s='323536546464654gregwgwwfw'
    for i in range(10):
        sn+=random.choice(s)
    sn+=datetime.now().strftime('%Y%m%d%H%M%S')
    return sn