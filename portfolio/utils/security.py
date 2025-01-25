import bleach
from bleach.css_sanitizer import CSSSanitizer

def sanitize_html(html_content):
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'strong', 'ul', 'p', 'br',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'pre', 'span'
    ]
    
    allowed_attrs = {
        'a': ['href', 'title'],
        'span': ['style'],
        # 'img': ['src', 'alt'] if you allow images
    }
    
    css_sanitizer = CSSSanitizer(
        allowed_css_properties={
            "color",
            "background-color",
            "font-weight",
            "font-style",
            "text-decoration",
            "font-size",
            "font-family"
        }
        # Remove allowed_css_functions since Bleach 6+ doesn't support it
    )

    clean_html = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        css_sanitizer=css_sanitizer,
        strip=True
    )
    return clean_html
