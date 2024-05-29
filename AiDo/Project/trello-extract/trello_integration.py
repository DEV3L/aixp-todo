from dotenv import load_dotenv

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
        print(f"Board: {board.name} (ID: {board.id})")
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
