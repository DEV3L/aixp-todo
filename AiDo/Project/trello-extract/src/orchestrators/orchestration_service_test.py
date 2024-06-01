from unittest.mock import MagicMock

from trello import Board

from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.orchestrators.orchestration_service import OrchestrationService
from src.services.trello_service import TrelloService


def test_get_board_markdown(mock_board: Board, trello_card: TrelloCard):
    expected_markdown = """# TODO

## List Name

To Do

## Labels

- Label1
- Label2

## Description

Test card description

## Comments

Test comment
"""

    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = mock_board
    mock_trello_service.extract_cards_info.return_value = CategorizedLists(todo=[trello_card])

    orchestration_service = OrchestrationService(mock_trello_service)
    markdown = orchestration_service.get_board_markdown("Test Board")

    assert markdown == expected_markdown

    mock_trello_service.get_board_by_name.assert_called_once_with("Test Board")
    mock_trello_service.extract_cards_info.assert_called_once_with(mock_trello_service.get_board_by_name.return_value)
