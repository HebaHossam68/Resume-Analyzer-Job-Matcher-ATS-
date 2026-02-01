NGROK_TOKEN="NGROK_AUTH_TOKEN_HERE"
from pyngrok import ngrok # type: ignore
ngrok.set_auth_token(NGROK_TOKEN)
public_url = ngrok.connect(8001)
print("API URL:", public_url)
