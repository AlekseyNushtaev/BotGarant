from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.environ.get("TG_TOKEN")
ADMIN_IDS = {int(x) for x in os.environ.get("ADMIN_IDS").split()}
