import os
import requests


SMM_API_URL = os.getenv("SMM_API_URL")
SMM_API_KEY = os.getenv("SMM_API_KEY")

SERVICE_1 = os.getenv("SMM_SERVICE_ID_1")
SERVICE_2 = os.getenv("SMM_SERVICE_ID_2")

QTY_1 = int(os.getenv("SMM_QUANTITY_1", 300))
QTY_2 = int(os.getenv("SMM_QUANTITY_2", 1000))


def place_order(service_id, link, quantity):
    try:
        payload = {
            "key": SMM_API_KEY,
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity
        }

        res = requests.post(SMM_API_URL, data=payload, timeout=10)
        return res.json()

    except Exception as e:
        print("SMM Error:", e)
        return None


# =========================
# 🚀 AUTO BOOST FUNCTION
# =========================
def boost_post(post_link):
    result = {}

    # Service 1
    result["service_1"] = place_order(SERVICE_1, post_link, QTY_1)

    # Service 2
    result["service_2"] = place_order(SERVICE_2, post_link, QTY_2)

    return result
