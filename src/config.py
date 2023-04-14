from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    webhook_url: str


@dataclass
class Config:
    tg: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg=TgBot(
            token=env.str("BOT_TOKEN"),
            webhook_url=env.str("WEBHOOK_URL")
        )
    )
