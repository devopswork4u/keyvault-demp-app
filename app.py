from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import traceback

from flask import render_template



app = Flask(__name__)

# Read environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME")

print(f"[DEBUG] Environment Variables:")
print(f"KEY_VAULT_URL = {KEY_VAULT_URL}")
print(f"SECRET_NAME = {SECRET_NAME}")

# Initialize client
credential = DefaultAzureCredential()
client = None
secret_value = "Not retrieved"

try:
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    secret = client.get_secret(SECRET_NAME)
    secret_value = secret.value
    print(f"[INFO] Retrieved secret: {SECRET_NAME}")
except Exception as e:
    print(f"[ERROR] Failed to retrieve secret: {str(e)}")
    traceback.print_exc()
    secret_value = f"ERROR: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html", secret_value=secret_value)

if __name__ == "__main__":
    app.run()
