from unittest.mock import MagicMock

from trello import Board
from trello import List as TrelloList

from src.services.categorized_list import CategorizedLists
from src.services.orchestration_service import OrchestrationService
from src.services.trello_card import TrelloCard
from src.services.trello_service import TrelloService


def test_get_all_card_data(mock_board: Board, categorized_lists: CategorizedLists[TrelloList], trello_card: TrelloCard):
    mock_trello_service = MagicMock(spec=TrelloService)
    mock_trello_service.get_board_by_name.return_value = mock_board
    mock_trello_service.categorize_lists.return_value = categorized_lists
    mock_trello_service.extract_cards_info.return_value = [trello_card]

    orchestration_service = OrchestrationService(trello_service=mock_trello_service)
    cards_info = orchestration_service.get_all_card_data("Test Board")

    assert len(cards_info) == 1

    card_info = cards_info[0]
    assert card_info.list_name == "To Do"
    assert card_info.description == "Test card description"
    assert card_info.labels == ["Label1", "Label2"]
    assert card_info.comments == ["Test comment"]
    assert card_info.due_date == ""

    mock_trello_service.get_board_by_name.assert_called_once_with("Test Board")
    mock_trello_service.categorize_lists.assert_called_once_with(mock_board)
    mock_trello_service.extract_cards_info.assert_called_once_with(categorized_lists)
