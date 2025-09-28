from flask import Flask, render_template
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SQLDB_PASSWORD = os.environ.get("SQLDB_PASSWORD")

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

try:
    secret_value = client.get_secret(SQLDB_PASSWORD).value
except Exception as e:
    secret_value = f"[Error] {str(e)}"

@app.route("/")
def index():
    return render_template("index.html", secret_value=secret_value)

if __name__ == "__main__":
    app.run()
