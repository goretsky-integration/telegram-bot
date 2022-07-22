from aiogram import executor

import handlers
from bot import dp, on_shutdown, on_startup


def main():
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_shutdown=on_shutdown,
        on_startup=on_startup,
    )


if __name__ == '__main__':
    main()
