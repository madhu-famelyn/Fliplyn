# import random
# import logging
# import requests

# logger = logging.getLogger(__name__)

# MSG91_AUTH_KEY = "459331Ak2ZMxxQ686ce706P1"

# MSG91_TEMPLATE_ID = "686cb8f4d6fc050e9c5603e2"  

# def generate_otp(length: int = 6) -> str:
#     """Generates a numeric OTP of desired length"""
#     return ''.join([str(random.randint(0, 9)) for _ in range(length)])
  

# def send_sms_otp(phone_number: str, otp: str) -> bool:
#     """
#     Sends an OTP to a phone number using MSG91 API and logs the result.
#     """
#     try:
#         url = "https://api.msg91.com/api/v5/otp"
#         headers = {
#             "authkey": MSG91_AUTH_KEY,
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "mobile": phone_number,
#             "otp": otp,
#             "template_id": MSG91_TEMPLATE_ID
#         }

#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()  # Will raise HTTPError for non-2xx responses
#         result = response.json()

#         # Check success or failure based on MSG91 response
#         if result.get("type") == "success":
#             message = f"[MSG91 ✅] OTP '{otp}' sent to {phone_number}. Response: {result}"
#             logger.info(message)
#             print(message)
#             return True
#         else:
#             message = f"[MSG91 ❌] Failed to send OTP to {phone_number}. MSG91 Error: {result}"
#             logger.error(message)
#             print(message)
#             return False

#     except Exception as e:
#         message = f"[MSG91 ❌] Exception while sending OTP to {phone_number}: {e}"
#         logger.error(message)
#         print(message)
#         return False
  


















import random
import logging
import requests
import json

# === SETUP LOGGING ===
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# === 2FACTOR CONFIG ===
TWO_FACTOR_API_KEY = "f924f073-639d-11f0-a562-0200cd936042"
TWO_FACTOR_TEMPLATE_NAME = "TemplateName1"  # Approved template name


# === MAILJET CONFIG ===
MAILJET_API_KEY = "a7d5d53211698766e2793da638ee4f18"
MAILJET_SECRET_KEY = "a9fd563a16be426bfcc139addfdd3cd4"
FROM_EMAIL = "madhu@famelyn.com"
FROM_NAME = "Neos OTP System"


# === COMMON FUNCTION ===
def generate_otp(length: int = 6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


# === SMS OTP via 2Factor ===
def send_sms_otp(phone_number: str, otp: str) -> bool:
    if not phone_number.startswith("91"):
        phone_number = "91" + phone_number

    url = (
        f"https://2factor.in/API/V1/{TWO_FACTOR_API_KEY}/SMS/{phone_number}/{otp}/{TWO_FACTOR_TEMPLATE_NAME}"
    )

    logger.debug(f"Sending 2Factor OTP to {phone_number} with OTP {otp}")
    try:
        response = requests.get(url)
        logger.debug("2Factor Response Status: %s", response.status_code)
        logger.debug("2Factor Response Body: %s", response.text)

        response.raise_for_status()
        result = response.json()

        if result.get("Status") == "Success":
            logger.info("[✅] SMS OTP sent via 2Factor to %s", phone_number)
            return True
        else:
            logger.warning("[⚠️] 2Factor OTP failed. Response: %s", result)
            return False

    except requests.exceptions.RequestException as e:
        logger.error("[❌] 2Factor Network Error: %s", e)
        return False
    except Exception as e:
        logger.error("[❌] 2Factor General Error: %s", e)
        return False


# === EMAIL OTP via MAILJET ===
def send_email_otp(to_email: str, otp: str) -> bool:
    url = "https://api.mailjet.com/v3.1/send"
    payload = {
        "Messages": [
            {
                "From": {
                    "Email": FROM_EMAIL,
                    "Name": FROM_NAME
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "User"
                    }
                ],
                "Subject": "Your OTP Code",
                "TextPart": f"Your OTP is: {otp}",
                "HTMLPart": f"<h3>Hello!</h3><p>Your OTP for verification is: <strong>{otp}</strong></p>"
            }
        ]
    }

    try:
        response = requests.post(
            url,
            auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
            json=payload
        )
        logger.debug("Mailjet Status Code: %s", response.status_code)
        logger.debug("Mailjet Body: %s", response.text)

        response.raise_for_status()
        result = response.json()

        if result["Messages"][0]["Status"] == "success":
            logger.info("[✅] Email OTP sent to %s", to_email)
            return True
        else:
            logger.warning("[⚠️] Email OTP failed. Response: %s", result)
            return False

    except requests.exceptions.RequestException as e:
        logger.error("[❌] Mailjet Network error: %s", e)
        return False
    except Exception as e:
        logger.error("[❌] Mailjet Error: %s", e)
        return False


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    otp = generate_otp()
    print(f"Generated OTP: {otp}")

    # Use either SMS or email
    send_sms_otp_2factor("9391176175", otp)  # ✅ 2Factor SMS OTP
    # send_email_otp("madhumithashanmugam2708@gmail.com", otp)  # ✅ Mailjet Email OTP
