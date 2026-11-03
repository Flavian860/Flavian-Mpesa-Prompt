import base64
from datetime import datetime
import requests
import streamlit as st

st.set_page_config(page_title="M-Pesa STK Push", page_icon="📲", layout="centered")

st.title("📲 M-Pesa Express (STK Push) Portal")
st.write("Trigger instant payment prompts directly to any Safaricom number.")

st.markdown("---")

# Input Fields
payer_phone = st.text_input(
    "Customer Phone Number", "2547", placeholder="e.g. 254712345678"
)
payment_amount = st.number_input(
    "Amount (KES)", min_value=1, value=100, step=1
)
payment_reason = st.text_input(
    "Payment Description / Reference", "Quick Payment"
)

if st.button("Send M-Pesa Prompt", type="primary"):
  if len(payer_phone) < 10 or not payer_phone.startswith("254"):
    st.error(
        "Please enter a valid phone number starting with 254 (e.g.,"
        " 2547XXXXXXXX)."
    )
  else:
    with st.spinner("Sending STK push prompt to phone..."):
      try:
        # Your Daraja Sandbox Credentials
        consumer_key = (
            "ssAPGQHWkClA0RH7SHa4h45pueSRJ0QOWHgBpGORyGGdK864"
        )
        consumer_secret = (
            "usOzSBt23Z6zjBWI9HbXP1JEMstlxV4jMzpNSwnXr8NcWSPyQowZPAPUTp817zsM"
        )
        business_shortcode = "174379"
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

        # 1. Generate Access Token
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        access_token = r.json().get("access_token")

        if not access_token:
          st.error("Failed to authenticate with Safaricom API.")
          st.stop()

        # 2. Prepare STK Push Payload
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{business_shortcode}{passkey}{timestamp}"
        encoded_password = base64.b64encode(password_str.encode()).decode(
            "utf-8"
        )

        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(payment_amount),
            "PartyA": payer_phone,
            "PartyB": business_shortcode,
            "PhoneNumber": payer_phone,
            "CallBackURL": "https://mydomain.com/callback",
            "AccountReference": "ExpressPay",
            "TransactionDesc": payment_reason,
        }

        response = requests.post(stk_url, json=payload, headers=headers)
        res_data = response.json()

        if res_data.get("ResponseCode") == "0":
          st.success(
              "✅ Prompt sent successfully! Check the phone for the M-Pesa PIN"
              " popup."
          )
          st.json(res_data)
        else:
          st.error(f"Failed to send prompt: {res_data}")

      except Exception as e:
        st.error(f"An error occurred: {e}")
payload = {
    "BusinessShortCode": business_shortcode,
    "Password": encoded_password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": int(payment_amount),
    "PartyA": payer_phone,
    "PartyB": business_shortcode,
    "PhoneNumber": payer_phone,
    "CallBackURL": "https://mydomain.com/callback",
    "AccountReference": "Flavian Joshua",  # Change this to what you want displayed
    "TransactionDesc": "Payment to Flavian",  # Change this description too
}
