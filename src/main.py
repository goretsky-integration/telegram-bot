from aiogram import executor

import handlers
from bot import dp, on_shutdown


def main():
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_shutdown=on_shutdown,
    )


if __name__ == '__main__':
    main()
