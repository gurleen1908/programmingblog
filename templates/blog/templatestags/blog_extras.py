import re
from django import template
from django.utils.html import escape

register = template.Library()


@register.filter
def format_blog_content(value):

    if not value:
        return ""

    text = str(value)

    # -----------------------------------------
    # Escape normal HTML for security
    # -----------------------------------------

    text = escape(text)

    # -----------------------------------------
    # Find code blocks
    #
    # ```javascript
    # code
    # ```
    # -----------------------------------------

    pattern = r"```(\w+)?\s*\n?(.*?)```"

    def replace_code(match):

        language = match.group(1) or "code"
        code = match.group(2).strip()

        return f"""
        <div class="professional-code-wrapper">

            <div class="code-header">

                <span class="code-language">
                    {language}
                </span>

                <button
                    type="button"
                    class="copy-code-btn"
                    onclick="copyCode(this)"
                >
                    Copy
                </button>

            </div>

            <pre><code>{code}</code></pre>

        </div>
        """

    text = re.sub(
        pattern,
        replace_code,
        text,
        flags=re.DOTALL
    )

    # -----------------------------------------
    # Convert remaining lines into paragraphs
    # -----------------------------------------

    parts = re.split(
        r"(<div class=\"professional-code-wrapper\">.*?</div>\s*</div>)",
        text,
        flags=re.DOTALL
    )

    result = ""

    for part in parts:

        if not part.strip():
            continue

        if "professional-code-wrapper" in part:

            result += part

        else:

            paragraphs = re.split(
                r"\n\s*\n",
                part
            )

            for paragraph in paragraphs:

                paragraph = paragraph.strip()

                if paragraph:

                    paragraph = paragraph.replace(
                        "\n",
                        "<br>"
                    )

                    result += f"""
                    <p class="article-paragraph">
                        {paragraph}
                    </p>
                    """

    return result