import mercadopago
from django.conf import settings
from requests.exceptions import ConnectionError, RequestException

mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

def create_preference(donation_amount, user_id):
    preference_data = {
        "items": [
            {
                "title": "Donación a Cáritas",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": donation_amount
            }
        ],
        "back_urls": {
            "success": "http://localhost:8000/donaciones/mercadopago_exito/" + str(user_id) + "/",
            "failure": "http://localhost:8000/donaciones/mercadopago_rechazo",
            "pending": "http://localhost:8000/donaciones/mercadopago_pendiente"
        },
        "auto_return": "approved",
    }
    
    try:
        preference = mp.preference().create(preference_data)
        return preference
    except (ConnectionError, RequestException) as e:
        print(f"Error al conectar con la API de MercadoPago: {e}")
        return None