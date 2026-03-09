class _SafeFormatDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def render_template(template_text: str, context: dict[str, object]) -> str:
    if not template_text:
        return ""

    safe_context = _SafeFormatDict(context)
    try:
        return template_text.format_map(safe_context)
    except (KeyError, ValueError, AttributeError):
        # Keep original text if braces are malformed or input is invalid.
        return template_text
