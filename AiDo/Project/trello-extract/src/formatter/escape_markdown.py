def escape_markdown(text: str) -> str:
    lines = text.split("\n")
    escaped_lines = []
    for line in lines:
        if line.startswith("#"):
            escaped_lines.append("##" + line)
        elif line.strip() == "---":
            escaped_lines.append("- - -")
        else:
            escaped_lines.append(line)
    return "\n".join(escaped_lines)
