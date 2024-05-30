from trello import Board, TrelloClient
from trello import List as TrelloList

from src.functions import first


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def get_lists_for_board(self, board: Board) -> list[TrelloList]:
        return board.all_lists()

    def get_board_by_name(self, board_name: str) -> Board:
        boards = self._list_boards()
        board = first(filter(lambda board: board.name == board_name, boards))

        if not board:
            raise RuntimeError(f"Board with name '{board_name}' not found.")

        return board

    def _list_boards(self) -> list[Board]:
        return self.client.list_boards()
