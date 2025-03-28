from templates import TEMPLATES

def generate_code(function_name, params):
    """Generate structured Python code dynamically using Jinja2 templates."""
    if function_name in TEMPLATES:
        return TEMPLATES[function_name].render(param1=params[0])
    else:
        return f"# ERROR: Function '{function_name}' not found in templates"
