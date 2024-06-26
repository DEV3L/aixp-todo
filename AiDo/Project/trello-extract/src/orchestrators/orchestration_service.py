import json
import os

from src.formatters.generate_markdown import generate_markdown
from src.services.trello_service import TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        self.trello_service = trello_service

    def write_board_markdown_to_file(self, board_name: str, directory: str) -> str:
        markdown_content = self.get_board_markdown(board_name)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{board_name} Status Trello Board.txt")
        with open(file_path, "w") as file:
            file.write(markdown_content)
        return file_path

    def get_board_markdown(self, board_name: str) -> str:
        board = self.trello_service.get_board_by_name(board_name)
        return generate_markdown(self.trello_service.extract_cards_info(board))

    def write_board_json_to_file(self, board_name: str, directory: str) -> str:
        board_json = self.get_board_json(board_name)

        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{board_name} Trello.json")
        with open(file_path, "w") as file:
            json.dump(board_json, file, indent=2)

        return file_path

    def get_board_json(self, board_name: str):
        board = self.trello_service.get_board_by_name(board_name)
        categorized_lists = self.trello_service.extract_cards_info(board)
        return categorized_lists.to_dict()
