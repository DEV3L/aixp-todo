from dataclasses import fields

from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.formatter.escape_markdown import escape_markdown


def get_dataclass_attributes(dataclass_type):
    return [field.name for field in fields(dataclass_type)]


class MarkdownService:
    def generate_markdown(self, categorized_list: CategorizedLists[TrelloCard]) -> str:
        list_items = [
            (category, cards)
            for (category, cards) in categorized_list.__dict__.items()
            if category in get_dataclass_attributes(CategorizedLists) and cards
        ]

        markdown_lines = []
        for category, cards in list_items:
            cards = getattr(categorized_list, category)

            markdown_lines.append(f"# {category.upper()}")
            markdown_lines.append("")

            for card in cards:
                if card.list_name:
                    markdown_lines.append("## List Name")
                    markdown_lines.append("")
                    markdown_lines.append(f"{card.list_name}")
                    markdown_lines.append("")

                if card.labels:
                    markdown_lines.append("## Labels")
                    markdown_lines.append("")
                    for label in card.labels:
                        markdown_lines.append(f"- {label}")
                    markdown_lines.append("")

                if card.due_date:
                    markdown_lines.append("## Due Date")
                    markdown_lines.append("")
                    markdown_lines.append(f"{card.due_date}")
                    markdown_lines.append("")

                if card.description:
                    markdown_lines.append("## Description")
                    markdown_lines.append("")
                    markdown_lines.append(escape_markdown(card.description))
                    markdown_lines.append("")

                if card.comments:
                    markdown_lines.append("## Comments")
                    markdown_lines.append("")
                    for comment in card.comments:
                        markdown_lines.append(escape_markdown(comment))
                        markdown_lines.append("")

        return "\n".join(markdown_lines)
