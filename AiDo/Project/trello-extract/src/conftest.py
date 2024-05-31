from unittest.mock import MagicMock

import pytest
from trello import Board, TrelloClient
from trello import List as TrelloList


@pytest.fixture
def mock_trello_client():
    return MagicMock(spec=TrelloClient)


def build_trello_list(list_name: str):
    trello_list = MagicMock(spec=TrelloList)
    trello_list.name = list_name
    return trello_list


@pytest.fixture
def mock_board():
    all_lists = [
        "Icebox",
        "Epics",
        "Backlog",
        "Doing",
        "Done 🎉",
        "Virtual Team",
        "Product",
        "Target User Personas",
        "_",
    ]

    board = MagicMock(spec=Board)
    board.all_lists.return_value = [build_trello_list(list_name) for list_name in all_lists]
    return board
