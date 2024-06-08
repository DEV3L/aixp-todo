from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.formatters.escape_markdown import escape_markdown


def generate_markdown(categorized_lists: CategorizedLists[TrelloCard]) -> str:
    list_items = [
        (category, cards)
        for category, cards in categorized_lists.__dict__.items()
        if category in categorized_lists.__dataclass_fields__ and cards
    ]

    markdown_lines = [line for category, cards in list_items for line in format_category(category, cards)]
    return "\n".join(markdown_lines)


def format_category(category: str, cards: list[TrelloCard]):
    return [
        f"# {category.upper()}\n\nThis is a list of cards, work items, user stories, and tasks that are in the {category} category.",
        "",
    ] + [line for card in cards for line in format_card(card)]


def format_card(card: TrelloCard):
    title_lines = [f"## Title: {card.title}", ""] if card.title else []
    list_name_lines = [f"## List Name: {card.list_name}", ""] if card.list_name else []
    labels_lines = ["## Labels", ""] + [f"- {label}" for label in card.labels] + [""] if card.labels else []
    done_date_lines = [f"## Done Date: {card.done_date}", ""] if card.done_date else []
    description_lines = ["## Description", "", escape_markdown(card.description), ""] if card.description else []
    comments_lines = (
        ["### Comments", ""] + [f"{escape_markdown(comment)}\n" for comment in card.comments] if card.comments else []
    )

    return title_lines + list_name_lines + labels_lines + done_date_lines + description_lines + comments_lines
