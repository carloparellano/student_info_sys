from dotenv import load_dotenv
from ssis import create_app

load_dotenv('.env')

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)