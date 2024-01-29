import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from src import load_config
from src.handlers import register_routes
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)

config = load_config(".env")

WEBHOOK_PATH = f"/bot/{config.tg.token}"
WEBHOOK_URL = config.tg.webhook_url + WEBHOOK_PATH

storage = MemoryStorage()

bot = Bot(token=config.tg.token, parse_mode="HTML")
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL)

    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)

# Register middlewares
dp.update.middleware(ConfigMiddleware(config))

# Register routes
register_routes(dp)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
