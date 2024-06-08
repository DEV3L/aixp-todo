from src.formatters.escape_markdown import escape_markdown


def test_escape_markdown():
    input_text = """# Heading
Some text
---
Another line
## Another heading
---
### Final heading"""

    expected_output = """#### Heading
Some text
- - -
Another line
##### Another heading
- - -
###### Final heading"""

    assert escape_markdown(input_text) == expected_output


def test_escape_markdown_max_heading_level():
    input_text = "#### Heading"

    expected_output = "###### Heading"

    assert escape_markdown(input_text) == expected_output
