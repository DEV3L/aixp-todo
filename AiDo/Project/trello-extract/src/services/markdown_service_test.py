from datetime import datetime
from typing import Literal

import pytest

from src.dataclasses.categorized_list import CategorizedLists
from src.dataclasses.trello_card import TrelloCard
from src.services.markdown_service import MarkdownService


@pytest.fixture(name="service")
def markdown_service() -> MarkdownService:
    return MarkdownService()


def test_headers(service: MarkdownService):
    expected_markdown = """# TODO

# DOING

# DONE
"""

    categorized_list = CategorizedLists(
        todo=[build_trello_card()],
        doing=[build_trello_card()],
        done=[build_trello_card()],
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_list_names(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## List Name

Task 2
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="Task 1"),
            build_trello_card(list_name="Task 2"),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_labels(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## Labels

- bug
- urgent
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="Task 1", labels=["bug", "urgent"]),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_due_date(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## Due Date

2024-05-01 00:00:00
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                list_name="Task 1",
                due_date=datetime(2024, 5, 1, 0, 0),
            ),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_descriptions(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## Description

Description of task 1

## List Name

Task 2

## Description

### Description of task 2
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="Task 1", description="Description of task 1"),
            build_trello_card(list_name="Task 2", description="# Description of task 2"),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_card_comments(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## Comments

- - -

Comment 1
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="Task 1", comments=["---", "Comment 1"]),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def test_generate_markdown(service: MarkdownService):
    expected_markdown = """# TODO

## List Name

Task 1

## Labels

- bug
- urgent

## Due Date

2024-05-01 00:00:00

## Description

Description of task 1

## Comments

Comment 1
"""

    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                list_name="Task 1",
                labels=["bug", "urgent"],
                due_date=datetime(2024, 5, 1, 0, 0),
                description="Description of task 1",
                comments=["Comment 1"],
            ),
        ]
    )

    markdown = service.generate_markdown(categorized_list)

    assert markdown == expected_markdown


def build_trello_card(
    *,
    list_name="",
    description="",
    labels: list[str] = [],
    comments: list[str] = [],
    due_date: datetime | Literal[""] = "",
):
    return TrelloCard(
        list_name=list_name,
        description=description,
        labels=labels,
        comments=comments,
        due_date=due_date,
    )
