# config.py
import os

TOKEN_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token"
CLIENT_ID = "fec253ea-0d06-4272-a5e6-b478baeecd70"
SCOPE = "openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access"

USERNAME = os.getenv("ERCOT_USERNAME")
PASSWORD = os.getenv("ERCOT_PASSWORD")
SUBSCRIPTION_KEY = os.getenv("ERCOT_SUB_KEY")

BASE_URL = "https://api.ercot.com/api"
