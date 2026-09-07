import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def format_blog_content(value):

    if not value:
        return ""

    text = str(value)

    # Code blocks:
    # ```javascript
    # code
    # ```
    pattern = r"```(\w+)?\s*\n?(.*?)```"

    def replace_code(match):

        language = match.group(1) or "code"
        code = match.group(2).strip()

        return f"""
        <div class="professional-code-block">

            <div class="code-header">
                <span class="code-language">{escape(language)}</span>

                <button type="button"
                        class="copy-code-btn"
                        onclick="copyCode(this)">
                    Copy
                </button>
            </div>

            <pre><code>{escape(code)}</code></pre>

        </div>
        """

    # Code blocks temporarily replace
    parts = []
    last_end = 0

    for match in re.finditer(pattern, text, flags=re.DOTALL):

        normal_text = text[last_end:match.start()]

        if normal_text.strip():
            paragraphs = normal_text.strip().split("\n\n")

            for paragraph in paragraphs:
                if paragraph.strip():
                    parts.append(
                        f'<p class="article-paragraph">{escape(paragraph.strip()).replace(chr(10), "<br>")}</p>'
                    )

        parts.append(replace_code(match))

        last_end = match.end()

    # Remaining text
    remaining = text[last_end:]

    if remaining.strip():

        paragraphs = remaining.strip().split("\n\n")

        for paragraph in paragraphs:
            if paragraph.strip():
                parts.append(
                    f'<p class="article-paragraph">{escape(paragraph.strip()).replace(chr(10), "<br>")}</p>'
                )

    return mark_safe("\n".join(parts))