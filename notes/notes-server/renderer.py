import mistune

_render = mistune.Markdown()


def render_target(target_file_path):
    """Renders a markdown file to HTML 
    """
    with open(target_file_path, "r") as in_file:
        md = in_file.read()
    return _render(md)
