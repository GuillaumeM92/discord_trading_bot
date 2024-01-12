import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    bot_token = os.getenv("BOT_TOKEN")


settings = Settings()
