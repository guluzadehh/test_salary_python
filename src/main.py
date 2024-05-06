import asyncio
import json
import os
import pydantic
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from app import App
from schemas import InputSchema

load_dotenv()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hi.!")


@dp.message()
async def total_salary_handler(message: Message) -> None:
    app = App()

    try:
        input = json.loads(message.text)
        request = InputSchema.model_validate(input)
        res = await app.run(request)
        data = res.model_dump()
        await message.answer(json.dumps(data, separators=(", ", ": ")))
    except (pydantic.ValidationError, json.JSONDecodeError) as e:
        print(e)
        await message.answer(
            'Невалидный запос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
        )
    except Exception as e:
        print(e)
        await message.answer("Произошла ошибка")


async def main() -> None:
    bot = Bot(token=os.getenv("BOT_TOKEN"))

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
