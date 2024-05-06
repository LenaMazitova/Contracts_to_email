import os
from dotenv import load_dotenv

load_dotenv(override=True)

SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
PATH_FOR_TABLE = str(os.environ.get('C:\\Users\\Elena\\Desktop\\Tests\\Contracts_to_email-1\\my_table.html'))

