from unittest.mock import MagicMock

import pytest
from trello import Board, TrelloClient

from src.services.trello_service import TrelloService


def test_get_board_by_name_found():
    mock_client = MagicMock(spec=TrelloClient)
    mock_board = MagicMock(spec=Board)
    mock_board.name = "Test Board"
    mock_client.list_boards.return_value = [mock_board]

    service = TrelloService(client=mock_client)

    result = service.get_board_by_name("Test Board")

    assert result == mock_board


def test_get_board_by_name_not_found():
    mock_client = MagicMock(spec=TrelloClient)
    mock_client.list_boards.return_value = []

    service = TrelloService(client=mock_client)

    with pytest.raises(RuntimeError, match="Board with name 'Nonexistent Board' not found."):
        service.get_board_by_name("Nonexistent Board")
