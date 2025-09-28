from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import traceback

app = Flask(__name__)

# Get Key Vault details from environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL", "MISSING_KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME", "MISSING_SECRET_NAME")

# Log environment variables for debugging (you’ll see these in Azure log stream)
print(f"[DEBUG] KEY_VAULT_URL = {KEY_VAULT_URL}")
print(f"[DEBUG] SECRET_NAME = {SECRET_NAME}")

# Set up the credential and Key Vault client
credential = DefaultAzureCredential()
client = None
secret_value = None

# Attempt to fetch the secret from Key Vault
try:
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    secret = client.get_secret(SECRET_NAME)
    secret_value = secret.value
    print(f"[INFO] Successfully retrieved secret: {SECRET_NAME}")
except Exception as e:
    print(f"[ERROR] Failed to retrieve secret: {SECRET_NAME}")
    traceback.print_exc()
    secret_value = f"[ERROR] Could not fetch secret: {str(e)}"

# Flask route
@app.route("/")
def index():
    return f"""
    <h1>Azure Key Vault Secret Demo</h1>
    <p><strong>Secret Name:</strong> {SECRET_NAME}</p>
    <p><strong>Secret Value:</strong> {secret_value}</p>
    """

# Run locally (only used for local dev, not in Azure App Service)
if __name__ == "__main__":
    app.run(debug=True)
