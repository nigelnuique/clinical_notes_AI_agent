# processor/utils.py

import base64

def strip_markdown_codeblock(text: str) -> str:
    """
    Removes ```json ... ``` or other code block markdown formatting.
    """
    if text.strip().startswith("```"):
        lines = text.strip().splitlines()
        return "\n".join(lines[1:-1]).strip()
    return text.strip()








