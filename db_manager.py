import time
from collections import defaultdict

# ======================
# قاعدة بيانات داخلية
# ======================
users_gold = defaultdict(int)
users_last_gift = defaultdict(float)
users_inventory = defaultdict(list)

# ======================
# الرصيد
# ======================
def get_user_gold(uid):
    return users_gold[uid]

def update_user_gold(uid, amount):
    users_gold[uid] += amount
    if users_gold[uid] < 0:
        users_gold[uid] = 0
    return users_gold[uid]

# ======================
# الهدايا اليومية
# ======================
def can_take_gift(uid):
    now = time.time()
    last = users_last_gift[uid]
    return now - last >= 86400  # 24 ساعة

def take_gift(uid, amount=100):
    # تأثير خوذة الحكيم أو تميمة الحظ
    bonus = 0
    if "خوذة الحكيم" in users_inventory[uid]:
        bonus += 50
    if "تميمة الحظ" in users_inventory[uid]:
        import random
        bonus += random.randint(50, 150)

    if can_take_gift(uid):
        users_last_gift[uid] = time.time()
        total = amount + bonus
        return update_user_gold(uid, total)
    else:
        return None

# ======================
# المخزون (Inventory)
# ======================
def add_item(uid, item):
    users_inventory[uid].append(item)
    return users_inventory[uid]

def get_inventory(uid):
    return users_inventory[uid]
