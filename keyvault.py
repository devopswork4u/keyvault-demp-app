from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

# Get Key Vault URL and secret name from environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME")

# Use managed identity to get the secret
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
try:
    secret_value = client.get_secret(SECRET_NAME).value
except Exception as e:
    secret_value = f"Failed to retrieve secret: {str(e)}"

@app.route("/")
def index():
    return f"<h1>Secret:</h1><p>{secret_value}</p>"

if __name__ == "__main__":
    app.run()
