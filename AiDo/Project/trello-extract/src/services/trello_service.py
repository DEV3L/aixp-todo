from trello import Board, TrelloClient


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def get_board_by_name(self, board_name: str) -> Board:
        boards = self._list_boards()
        matching_boards = list(filter(lambda board: board.name == board_name, boards))
        if not matching_boards:
            raise RuntimeError(f"Board with name '{board_name}' not found.")
        return matching_boards[0]

    def _list_boards(self) -> list[Board]:
        return self.client.list_boards()
