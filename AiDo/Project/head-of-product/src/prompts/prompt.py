from datetime import datetime

from ai_assistant_manager.encoding import UTF_8

PROMPT_PATH = "src/prompts/prompt.md"

CURRENT_DATE_VARIABLE = "{{CURRENT_DATE}}"


def get_prompt():
    with open(PROMPT_PATH, "r", encoding=UTF_8) as prompt:
        current_date = datetime.today().date().isoformat()
        return prompt.read().replace(CURRENT_DATE_VARIABLE, current_date)
