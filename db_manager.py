import json
import time
import os

DATA_FILE = "bot_data.json"

# ======================
# تحميل البيانات من الملف
# ======================
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {
        "users_gold": {},
        "users_inventory": {},
        "users_last_gift": {}
    }

# ======================
# حفظ البيانات للملف
# ======================
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ======================
# الرصيد
# ======================
def get_user_gold(uid):
    return data["users_gold"].get(str(uid), 0)

def update_user_gold(uid, amount):
    uid = str(uid)
    current = data["users_gold"].get(uid, 0)
    current += amount
    if current < 0:
        current = 0
    data["users_gold"][uid] = current
    save_data()
    return current

# ======================
# المخزون (Inventory)
# ======================
def add_item(uid, item):
    uid = str(uid)
    inv = data["users_inventory"].get(uid, [])
    inv.append(item)
    data["users_inventory"][uid] = inv
    save_data()
    return inv

def get_inventory(uid):
    return data["users_inventory"].get(str(uid), [])

# ======================
# الهدايا اليومية
# ======================
def can_take_gift(uid):
    uid = str(uid)
    now = time.time()
    last = data["users_last_gift"].get(uid, 0)
    return now - last >= 86400  # 24 ساعة

def take_gift(uid, amount=100):
    uid = str(uid)
    if can_take_gift(uid):
        data["users_last_gift"][uid] = time.time()

        bonus = 0
        inv = get_inventory(uid)
        if "خوذة الحكيم" in inv:
            bonus += 50
        if "تميمة الحظ" in inv:
            import random
            bonus += random.randint(50, 150)

        total = amount + bonus
        update_user_gold(uid, total)
        return total
    else:
        return None
