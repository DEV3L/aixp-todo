from src.formatter.generate_markdown import generate_markdown
from src.services.trello_service import TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        self.trello_service = trello_service

    def get_board_markdown(self, board_name: str) -> str:
        board = self.trello_service.get_board_by_name(board_name)
        return generate_markdown(self.trello_service.extract_cards_info(board))
