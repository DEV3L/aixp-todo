from datetime import datetime
from unittest.mock import MagicMock

import pytest
from trello import Board, Card, Label, TrelloClient
from trello import List as TrelloList

from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.services.trello_service import TrelloService


@pytest.fixture
def trello_service(mock_trello_client: TrelloClient):
    return TrelloService(client=mock_trello_client)


@pytest.fixture
def categorized_lists(mock_trello_list: MagicMock):
    return CategorizedLists[TrelloList](todo=[mock_trello_list], doing=[], done=[])


@pytest.fixture
def trello_card():
    return TrelloCard(
        list_name="To Do",
        description="Test card description",
        labels=["Label1", "Label2"],
        comments=["Test comment"],
        due_date="",
    )


@pytest.fixture
def mock_trello_client():
    return MagicMock(spec=TrelloClient)


@pytest.fixture
def mock_board():
    def build_trello_list(list_name: str):
        trello_list = MagicMock(spec=TrelloList)
        trello_list.name = list_name
        return trello_list

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
    board.name = "Test Board"
    board.all_lists.return_value = [build_trello_list(list_name) for list_name in all_lists]
    return board


@pytest.fixture
def mock_trello_list():
    mock_list = MagicMock(spec=TrelloList)
    mock_list.name = "Doing"
    return mock_list


@pytest.fixture
def mock_card():
    label_one = MagicMock(spec=Label)
    label_one.name = "Label1"
    label_two = MagicMock(spec=Label)
    label_two.name = "Label2"

    mock_card = MagicMock(spec=Card)
    mock_card.name = "Test Card"
    mock_card.description = "Test card description"
    mock_card.labels = [label_one, label_two]
    mock_card.comments = [{"data": {"text": "Test comment"}}]
    mock_card.due_date = datetime(2023, 1, 1)
    return mock_card
