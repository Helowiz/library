from dotenv import load_dotenv
from flask_cors import CORS
from core.main import create_app

load_dotenv()
app = create_app()
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
