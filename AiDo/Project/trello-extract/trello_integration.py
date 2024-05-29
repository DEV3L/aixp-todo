import os

from dotenv import load_dotenv
from trello import TrelloClient

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")


def main():
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_TOKEN,
    )

    # Get all boards
    boards = client.list_boards()
    print("Boards:")
    for board in boards:
        print(f"- {board.name} (ID: {board.id})")


if __name__ == "__main__":
    main()
