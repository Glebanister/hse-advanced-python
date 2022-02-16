import operator

from typing import List, Any, Union, Tuple
from functools import reduce

import latex


def centered(*sources: latex.Syntax) -> latex.Block:
    return latex.Block('center', latex.print_syntax(*sources))


def document(*sources: latex.Syntax) -> latex.Block:
    return latex.Block('document', latex.print_syntax(*sources))


FormatRow = Tuple[List[latex.Source], latex.OptFmtRow]


def table(rows_and_formats: Tuple[latex.OptFmtRow, List[FormatRow]],
          col_intervals: List[latex.OptFmtCol]
          ) -> latex.Table:

    first_row_format, format_rows = rows_and_formats

    rows = list(map(lambda item: item[0], format_rows))
    formats_tail = map(lambda item: item[1], format_rows)
    rows_formats = [first_row_format] + list(formats_tail)

    n_cols = len(rows[0])

    def check_row(row: List[latex.Source]) -> None:
        row_list = list(row)
        if len(row_list) != n_cols:
            raise Exception('Not all rows has same amount of columns. '
                            f'First row length: {n_cols}, current: {len(row_list)}')

    map(check_row, rows)

    if len(col_intervals) != n_cols + 1:
        raise Exception('List of column formats must be n_cols + 1')

    n_rows = len(rows)
    return latex.Table(n_rows, n_cols, rows_formats, col_intervals, rows)


def table_simple(rows: List[List[Any]],
                 *,
                 separate_rows: bool,
                 separate_cols: bool) -> latex.Table:
    formatted_rows = list(map(lambda row: list(
        map(lambda x: latex.Source(str(x)), row)), rows))

    row_separator = None if not separate_rows else latex.FormatIntervalRow.single
    row_separators_tail = [row_separator] * len(rows)
    rows_and_formats = list(zip(formatted_rows, row_separators_tail))

    col_separator = None if not separate_cols else latex.FormatIntervalCol.single
    col_separators = [col_separator] * (len(rows[0]) + 1)
    return table((row_separator, rows_and_formats), col_separators)
