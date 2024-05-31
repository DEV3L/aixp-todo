from dotenv import load_dotenv
from loguru import logger

from src.clients.trello_client import get_trello_client
from src.orchestrators.orchestration_service import OrchestrationService
from src.services.trello_service import TrelloService
from src.settings import get_settings

load_dotenv()


def main():
    settings = get_settings()
    orchestration_service = OrchestrationService(TrelloService(get_trello_client(settings)))

    try:
        all_cards = orchestration_service.get_all_card_data(settings.trello_board_name)
        for card in all_cards:
            logger.info(f"Card: {card})")
    except RuntimeError as e:
        logger.error(e)


if __name__ == "__main__":
    main()
