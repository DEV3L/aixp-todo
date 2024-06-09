from datetime import datetime

from src.prompts.prompt import get_prompt


def test_get_prompt():
    current_date = datetime.today().date().isoformat()

    prompt = get_prompt()
    assert isinstance(prompt, str)
    assert current_date in prompt
