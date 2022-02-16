import latex

def plain(content: str) -> latex.Text:
    return latex.Text(content)

def endl() -> latex.Text:
    return plain('\\\\')

def space() -> latex.Text:
    return plain('\\')
