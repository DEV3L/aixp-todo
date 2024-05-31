from functools import reduce

from trello import Board, TrelloClient
from trello import List as TrelloList

from src.functions import first
from src.services.categorized_list import CategorizedLists


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def categorize_lists(self, board: Board):
        trello_lists = self.get_lists_for_board(board)
        filtered_trello_lists = filter(lambda trello_list: "_" != trello_list.name, trello_lists)

        return reduce(reducer, filtered_trello_lists, CategorizedLists[TrelloList](todo=[], doing=[], done=[]))

    def get_board_by_name(self, board_name: str) -> Board:
        boards = self._list_boards()
        board = first(filter(lambda board: board.name == board_name, boards))

        if not board:
            raise RuntimeError(f"Board with name '{board_name}' not found.")

        return board

    def get_lists_for_board(self, board: Board) -> list[TrelloList]:
        return board.all_lists()

    def _list_boards(self) -> list[Board]:
        return self.client.list_boards()


def reducer(accumulator: CategorizedLists, trello_list: TrelloList):
    if trello_list.name in ["Icebox", "Epics"]:
        accumulator.todo.append(trello_list)
    elif trello_list.name in ["Backlog", "Doing"]:
        accumulator.doing.append(trello_list)
    else:
        accumulator.done.append(trello_list)
    return accumulator
