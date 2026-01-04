import time
from collections import defaultdict

# قاعدة بيانات داخلية
users_gold = defaultdict(int)
users_last_gift = defaultdict(float)

# الرصيد
def get_user_gold(uid):
    return users_gold[uid]

def update_user_gold(uid, amount):
    users_gold[uid] += amount
    if users_gold[uid] < 0:
        users_gold[uid] = 0
    return users_gold[uid]

# الهدايا اليومية
def can_take_gift(uid):
    now = time.time()
    last = users_last_gift[uid]
    return now - last >= 86400  # 24 ساعة

def take_gift(uid, amount=100):
    if can_take_gift(uid):
        users_last_gift[uid] = time.time()
        return update_user_gold(uid, amount)
    else:
        return None
