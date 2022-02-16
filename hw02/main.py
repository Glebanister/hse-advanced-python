from pathlib import Path
from typing import List

import latex
import defaults.commands as command
import defaults.blocks as block
import defaults.text as text


def default_document(*sources: latex.Syntax):
    return latex.print_syntax(
        command.documentclass('article'),
        command.usepackage_params({'margin': '0.7in'}, ['geometry']),
        command.usepackage_params({'parfill': None}, ['parskip']),
        command.usepackage_params({'utf8': None}, ['inputenc']),
        command.usepackage('amsmath', 'amssymb', 'amsfonts', 'amsthm'),

        block.document(
            *sources
        )
    )


def latex_advanced():
    return default_document(
        command.section('This is test for latex printer'),
        command.subsection('Plain text'),
        text.plain('Hello!'),
        command.subsection('Centered text'),
        block.centered(
            text.plain('Some text in the center')
        ),
        command.subsection('Table'),
        block.centered(
            block.table_simple([[1, 2, 3], [4, 5, 6]],
                               separate_rows=True,
                               separate_cols=True)
        ),
        command.subsection('Average number of animals per household'),
        block.table(
            (latex.FormatIntervalRow.single,
             [
                 (['', 'Russia', 'USA', 'UK', 'Australia', 'China'],
                  latex.FormatIntervalRow.double),
                 (['Cats', '0.5', '1.0', '2.9', '0.6', '4.9'],
                  None),
                 (['Dogs', '10.5', '6.3', '29.1', '10.6', '0.09'],
                  None),
                 (['Snakes', '0.001', '0.4', '0.65', '213.5', '1.13'],
                  latex.FormatIntervalRow.single),
             ]),
            [
                latex.FormatIntervalCol.single,
                latex.FormatIntervalCol.double,
                None,
                None,
                None,
                None,
                latex.FormatIntervalCol.single,
            ])
    )


def latex_table_easy():
    return default_document(
        block.centered(
            block.table_simple([[1, 2, 3], [4, 5, 6]],
                               separate_rows=True,
                               separate_cols=True)
        )
    )


def latex_with_image(images_root_paths: List[Path], images_rel_pahts: List[Path]):
    return latex.print_syntax(
        command.documentclass('article'),
        command.usepackage_params({'margin': '0.7in'}, ['geometry']),
        command.usepackage_params({'parfill': None}, ['parskip']),
        command.usepackage_params({'utf8': None}, ['inputenc']),
        command.usepackage('amsmath', 'amssymb', 'amsfonts', 'amsthm'),
        command.usepackage('graphicx'),
        command.graphicspath(images_root_paths),

        block.document(
            *map(lambda img: command.includegraphics(img, width='\\textwidth'), images_rel_pahts)
        )
    )


def main():
    print(latex_with_image([Path('.').absolute()], [Path('puppy.jpeg')]))


if __name__ == '__main__':
    main()
