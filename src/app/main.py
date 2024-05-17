import asyncio
import logging
import sys

from app.server import Server


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    server = Server()
    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
