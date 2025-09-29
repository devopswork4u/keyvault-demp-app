from flask import Flask, render_template
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import traceback

app = Flask(__name__)

# Read environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAMES = [
    os.environ.get("SQLDB_PASSWORD")
]

# Initialize client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Dictionary to hold secret name -> value
secrets_dict = {}

try:
    for secret_name in SECRET_NAMES:
        if secret_name:
            secret = client.get_secret(secret_name)
            secrets_dict[secret_name] = secret.value
            print(f"[INFO] Retrieved secret: {secret_name}")
        else:
            print(f"[WARN] Missing environment variable for secret name.")
except Exception as e:
    print(f"[ERROR] Failed to retrieve secrets: {str(e)}")
    traceback.print_exc()
    secrets_dict = {"ERROR": str(e)}

@app.route("/")
def index():
    return render_template("index.html", secrets=secrets_dict)

if __name__ == "__main__":
    app.run()