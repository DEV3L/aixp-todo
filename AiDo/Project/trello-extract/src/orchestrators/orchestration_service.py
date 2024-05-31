from src.services.trello_service import TrelloCard, TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        self.trello_service = trello_service

    def get_all_card_data(self, board_name: str) -> list[TrelloCard]:
        board = self.trello_service.get_board_by_name(board_name)
        categorized_lists = self.trello_service.categorize_lists(board)
        return self.trello_service.extract_cards_info(categorized_lists)
