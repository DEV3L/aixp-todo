from dotenv import load_dotenv
from loguru import logger

from src.clients.trello_client import get_trello_client
from src.services.trello_service import TrelloService
from src.settings import get_settings

load_dotenv()


def main():
    settings = get_settings()

    client = get_trello_client(settings)
    service = TrelloService(client)

    try:
        board = service.get_board_by_name(settings.trello_board_name)
        logger.info(f"Board: {board.name} (ID: {board.id})")

        lists = service.get_lists_for_board(board)
        for list in lists:
            logger.info(f"List: {list.name} (ID: {list.id})")
    except RuntimeError as e:
        logger.error(e)


if __name__ == "__main__":
    main()
