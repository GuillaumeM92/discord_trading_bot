import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    bot_token = os.getenv("BOT_TOKEN")
    polygon_api_key = os.getenv("POLYGON_API_KEY")


settings = Settings()
