import os, secrets
from dotenv import load_dotenv
from client import create_app

app = create_app()
load_dotenv()

app.secret_key = random_secret = secrets.token_hex(16)
app.config['DEBUG'] = os.environ.get("FLASK_DEBUG") == "1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8000)))