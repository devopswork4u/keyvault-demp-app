from flask import Flask, render_template
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

# Get environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SQLDB_SECRET_NAME = os.environ.get("SQLDB_SECRET_NAME")

# Check if both environment variables are set
if not KEY_VAULT_URL or not SQLDB_SECRET_NAME:
    secret_value = "[Error] Environment variables KEY_VAULT_URL or SQLDB_SECRET_NAME not set."
else:
    try:
        # Initialize credential and secret client
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # Fetch the secret value
        secret_value = client.get_secret(SQLDB_SECRET_NAME).value
    except Exception as e:
        secret_value = f"[Error] {str(e)}"

@app.route("/")
def index():
    return render_template("index.html", secret_value=secret_value)

if __name__ == "__main__":
    app.run(debug=True)
