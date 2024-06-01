from typing import List, Tuple

from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.formatter.escape_markdown import escape_markdown


def generate_markdown(categorized_list: CategorizedLists[TrelloCard]) -> str:
    def format_card(card: TrelloCard) -> List[str]:
        card_lines = []
        if card.list_name:
            card_lines.extend(["## List Name", "", card.list_name, ""])
        if card.labels:
            card_lines.extend(["## Labels", ""] + [f"- {label}" for label in card.labels] + [""])
        if card.due_date:
            card_lines.extend(["## Due Date", "", str(card.due_date), ""])
        if card.description:
            card_lines.extend(["## Description", "", escape_markdown(card.description), ""])
        if card.comments:
            card_lines.extend(["## Comments", ""] + [f"{escape_markdown(comment)}\n" for comment in card.comments])
        return card_lines

    def format_category(category: str, cards: List[TrelloCard]) -> List[str]:
        category_lines = [f"# {category.upper()}", ""]
        for card in cards:
            category_lines.extend(format_card(card))
        return category_lines

    list_items: List[Tuple[str, List[TrelloCard]]] = [
        (category, cards)
        for category, cards in categorized_list.__dict__.items()
        if category in categorized_list.__dataclass_fields__ and cards
    ]

    markdown_lines = [line for category, cards in list_items for line in format_category(category, cards)]
    return "\n".join(markdown_lines)
