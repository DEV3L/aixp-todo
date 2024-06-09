from loguru import logger

from src.assistants.assistant_service import (
    ASSISTANT_NAME,
    AssistantService,
)
from src.clients.openai_api import OpenAIClient, build_openai_client
from src.exporters.blogs.blogs_exporter import BlogsExporter
from src.exporters.files.file_exporter import FileExporter


def export_data():
    BlogsExporter().export()
    FileExporter("AiDo Product Definition.txt").export()
    FileExporter("AiDo Status Trello Board.txt").export()
    FileExporter("AiDo Website.txt").export()
    FileExporter("Persona - Head of Product - Alex Parker.txt").export()


def main():
    logger.info(f"Building {ASSISTANT_NAME}")

    export_data()

    client = OpenAIClient(build_openai_client())
    service = AssistantService(client)

    logger.info("Removing existing assistant and category files")
    service.delete_assistant()

    assistant_id = service.get_assistant_id()

    logger.info(f"Assistant ID: {assistant_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Error: {e}")
