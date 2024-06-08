def escape_markdown(text: str) -> str:
    return "\n".join(map(escape_line, text.split("\n")))


def escape_line(line: str) -> str:
    if line.startswith("#"):
        num_hashes = len(line) - len(line.lstrip("#"))
        num_hashes = min(num_hashes + 3, 6)
        return "#" * num_hashes + line.lstrip("#")

    if line.strip() == "---":
        return "- - -"

    return line
