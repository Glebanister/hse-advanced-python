from typing import Dict, Optional, List
from pathlib import Path

import latex
import utils


def documentclass(type: str) -> latex.Command:
    return latex.Command('documentclass', {}, type)


def usepackage_params(params: Dict[str, Optional[str]], args: List[str]) -> latex.Command:
    return latex.Command('usepackage', params, ','.join(args))


def usepackage(*args: str) -> latex.Command:
    return usepackage_params({}, [*args])


def graphicspath(images_paths: List[Path]) -> latex.Command:

    def format_image_path(path: Path) -> str:
        return utils.in_parent(str(path), utils.Parenthesis.curly)

    return latex.Command('graphicspath', {}, ''.join(map(format_image_path, images_paths)))


def includegraphics(
    image_path: Path,
    *,
    width: Optional[str] = None,
    height: Optional[str] = None
) -> latex.Command:
    params = utils.remove_null_keys({
        'width': width,
        'height': height
    })
    return latex.Command('includegraphics', params, str(image_path))


def section(name: str) -> latex.Command:
    return latex.Command('section', {}, name)


def subsection(name: str) -> latex.Command:
    return latex.Command('subsection', {}, name)
