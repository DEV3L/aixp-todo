from unittest.mock import MagicMock

import pytest
from trello import Board, TrelloClient
from trello import List as TrelloList

from src.services.trello_service import TrelloService


def test_categorize_lists(mock_trello_client: TrelloClient, mock_board: Board):
    service = TrelloService(mock_trello_client)
    categorized = service.categorize_lists(mock_board)

    assert len(categorized.todo) == 2
    assert len(categorized.doing) == 2
    assert len(categorized.done) == 4
    assert all("_" not in lst.name for lst in categorized.todo)
    assert all("_" not in lst.name for lst in categorized.doing)
    assert all("_" not in lst.name for lst in categorized.done)


def test_get_board_by_name_found(mock_trello_client: MagicMock):
    mock_board = MagicMock(spec=Board)
    mock_board.name = "Test Board"

    mock_trello_client.list_boards.return_value = [mock_board]

    service = TrelloService(client=mock_trello_client)

    result = service.get_board_by_name("Test Board")

    assert result == mock_board


def test_get_board_by_name_not_found(mock_trello_client: MagicMock):
    mock_trello_client.list_boards.return_value = []

    service = TrelloService(client=mock_trello_client)

    with pytest.raises(RuntimeError, match="Board with name 'Nonexistent Board' not found."):
        service.get_board_by_name("Nonexistent Board")


def test_get_lists_for_board(mock_trello_client: TrelloClient):
    mock_board = MagicMock(spec=Board)

    mock_lists = [MagicMock(spec=TrelloList) for _ in range(3)]
    mock_board.all_lists.return_value = mock_lists

    service = TrelloService(client=mock_trello_client)

    lists = service.get_lists_for_board(mock_board)

    assert lists == mock_lists
    mock_board.all_lists.assert_called_once()
