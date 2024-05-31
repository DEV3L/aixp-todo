from functools import reduce

from trello import Board, TrelloClient
from trello import List as TrelloList

from src.functions import first
from src.services.categorized_list import CategorizedLists
from src.services.trello_card import TrelloCard
from src.services.trello_utilities import extract_card_info, trello_list_reducer


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def extract_cards_info(self, categorized_lists: CategorizedLists[TrelloList]) -> list[TrelloCard]:
        """Extracts card information from categorized lists."""
        return [
            extract_card_info(trello_list, card)
            for trello_list in categorized_lists.todo + categorized_lists.doing + categorized_lists.done
            for card in trello_list.list_cards()
        ]

    def categorize_lists(self, board: Board) -> CategorizedLists[TrelloList]:
        """Categorizes lists from a board into todo, doing, and done."""
        trello_lists = self.get_lists_for_board(board)
        filtered_trello_lists = filter(lambda trello_list: "_" != trello_list.name, trello_lists)
        return reduce(
            trello_list_reducer, filtered_trello_lists, CategorizedLists[TrelloList](todo=[], doing=[], done=[])
        )

    def get_board_by_name(self, board_name: str) -> Board:
        """Retrieves a board by its name."""
        boards = self._list_boards()
        board = first(filter(lambda board: board.name == board_name, boards))

        if not board:
            raise RuntimeError(f"Board with name '{board_name}' not found.")

        return board

    def get_lists_for_board(self, board: Board) -> list[TrelloList]:
        """Gets all lists for a given board."""
        return board.all_lists()

    def _list_boards(self) -> list[Board]:
        """Lists all boards for the client."""
        return self.client.list_boards()
