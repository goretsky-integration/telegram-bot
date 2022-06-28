from aiogram import executor

import handlers
from bot import dp


def main():
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
