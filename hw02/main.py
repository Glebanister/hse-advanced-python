#!/usr/bin/env python3

import argparse

from pathlib import Path
from typing import List
from enum import Enum

import latex
import defaults.commands as command
import defaults.blocks as block
import defaults.text as text

import beautiful_ast.ast_visualizer as beautiful_ast


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
    return latex.print_syntax(
        command.documentclass('article'),
        command.usepackage_params({'margin': '0.7in'}, ['geometry']),
        command.usepackage_params({'parfill': None}, ['parskip']),
        command.usepackage_params({'utf8': None}, ['inputenc']),
        command.usepackage('amsmath', 'amssymb', 'amsfonts', 'amsthm'),
        command.usepackage('graphicx'),
        command.graphicspath([Path('..') / 'resources']),

        block.document(
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
                ]
            ),
            command.subsection('Note'),
            block.centered(
                text.plain('Please, scroll down for the puppy...')
            ),
            command.subsection('And finally, puppy!'),
            command.includegraphics(Path('puppy.jpeg'), width='\\textwidth')
        )
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
            command.section('Table'),
            block.centered(
                block.table_simple([[1, 2, 3], [4, 5, 6]],
                                   separate_rows=True,
                                   separate_cols=True)
            ),
            command.section('Image'),
            *map(lambda img: command.includegraphics(img, width='\\textwidth'), images_rel_pahts)
        )
    )


def latex_of_ast(root: Path):
    root.mkdir(exist_ok=True)
    out_path = root / 'fib_ast.png'
    beautiful_ast.visualize_from_source(
        "a = lambda n: 1 if n < 2 else a(n - 1) + a(n - 2)",
        out_path,
        no_show=True
    )
    return latex_with_image([root], [out_path.name])


class LatexContent(Enum):
    table = 'table'
    ast = 'ast'
    advanced = 'advanced'

    def __str__(self):
        return self.value


def main():
    arg_parser = argparse.ArgumentParser('LaTeX Generator')
    arg_parser.add_argument('content', type=LatexContent,
                            choices=list(LatexContent))
    arg_parser.add_argument('output', type=Path)
    args = arg_parser.parse_args()

    output = Path(args.output).with_suffix('.tex')
    generators = {
        LatexContent.ast: lambda: latex_of_ast(output.parent),
        LatexContent.advanced: latex_advanced,
        LatexContent.table: latex_table_easy
    }
    with open(output, 'w') as out_latex:
        out_latex.write(generators[args.content]())


if __name__ == '__main__':
    main()
