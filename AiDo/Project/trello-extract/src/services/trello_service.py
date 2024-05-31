from functools import reduce

from trello import Board, Card, TrelloClient
from trello import List as TrelloList

from src.functions import first
from src.services.categorized_list import CategorizedLists
from src.services.trello_card import TrelloCard


class TrelloService:
    def __init__(self, client: TrelloClient):
        self.client = client

    def extract_cards_info(self, categorized_lists: CategorizedLists[TrelloList]) -> list[TrelloCard]:
        return [
            extract_card_info(trello_list, card)
            for trello_list in categorized_lists.todo + categorized_lists.doing + categorized_lists.done
            for card in trello_list.list_cards()
        ]

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


def extract_card_info(trello_list: TrelloList, card: Card) -> TrelloCard:
    return TrelloCard(
        list_name=trello_list.name,
        description=card.description,
        labels=[label.name for label in card.labels],
        comments=[comment["data"]["text"] for comment in card.comments],
        due_date=card.due_date,
    )


def reducer(accumulator: CategorizedLists, trello_list: TrelloList):
    if trello_list.name in ["Icebox", "Epics"]:
        accumulator.todo.append(trello_list)
    elif trello_list.name in ["Backlog", "Doing"]:
        accumulator.doing.append(trello_list)
    else:
        accumulator.done.append(trello_list)
    return accumulator
