from typing import (
    NewType, Dict, Optional,
    Callable, Tuple,
    Type, Iterable, List, Any)
from dataclasses import dataclass
from enum import Enum

import utils


Source = NewType('Source', str)


@dataclass(frozen=True)
class Command:
    name: str
    options: Dict[str, Optional[str]]
    arguments: Optional[str]


@dataclass(frozen=True)
class Block:
    tag: str
    inner: Source


@dataclass(frozen=True)
class Sequence:
    elems: Iterable[Source]
    separator: str


@dataclass(frozen=True)
class Text:
    content: str


class FormatIntervalCol(Enum):
    single = '|'
    double = '||'


class FormatIntervalRow(Enum):
    single = '\\hline'
    double = '\\hline\\hline'


OptFmtCol = Optional[FormatIntervalCol]
OptFmtRow = Optional[FormatIntervalRow]


@dataclass(frozen=True)
class Table:
    n_rows: int
    n_cols: int
    fmt_rows: List[OptFmtRow]  # len(fmt_rows) = n_rows + 1
    fmt_cols: List[OptFmtCol]  # len(fmt_cols) = n_cols + 1
    data: List[List[Source]]  # n_rows x n_cols


Syntax = Any
SourcePrinter = Callable[[Any], Source]

_PRINTERS: Dict[Type, Callable[[Syntax], Source]] = {}


def printer(type: Type) -> Callable[[SourcePrinter], SourcePrinter]:
    def printer_with_func(func: SourcePrinter) -> SourcePrinter:
        _PRINTERS[type] = func
        return func
    return printer_with_func


@printer(Command)
def print_command(c: Command) -> Source:

    def format_option(item: Tuple[str, Optional[str]]):
        return item[0] if item[1] is None else f'{item[0]}={item[1]}'

    options: str = '' if c.options == {} else utils.in_parent(
        ','.join(map(format_option, c.options.items())),
        utils.Parenthesis.square)

    arguments = '' if c.arguments is None else utils.Parenthesis.curly.embrace(
        c.arguments)

    return Source(f'\\{c.name}{options}{arguments}')


@printer(Block)
def print_block(b: Block) -> Source:

    begin = Command('begin', {}, b.tag)
    end = Command('end', {}, b.tag)

    return Source(utils.lines(
        print_command(begin),
        b.inner,
        print_command(end)))


@printer(Sequence)
def print_sequence(seq: Sequence) -> Source:
    return Source(seq.separator.join(seq.elems))


@printer(Text)
def print_text(t: Text) -> Source:
    return Source(t.content)


@printer(Table)
def print_table(t: Table) -> Source:
    def print_col_format(fmt: OptFmtCol) -> str:
        return '' if fmt is None else fmt.value

    def print_row_format(fmt: OptFmtRow) -> Source:
        return Source('' if fmt is None else fmt.value)

    col_letters = 'c' * t.n_cols
    col_formats = map(print_col_format, t.fmt_cols)

    table_format_section = utils.in_parent(
        ' '.join(utils.intercalate(col_formats, col_letters)),
        utils.Parenthesis.curly
    )

    def format_table_row(row: Iterable[Source]) -> Source:
        return Source(str(print_sequence(Sequence(row, ' & '))) + '\\\\')

    row_sources = map(format_table_row, t.data)
    format_sources = map(print_row_format, t.fmt_rows)

    table_rows = filter(lambda r: r != '', utils.intercalate(format_sources, row_sources))

    table_content = print_sequence(
        Sequence(table_rows,
                 separator='\n')
    )

    return print_block(Block('tabular', Source(utils.lines(table_format_section, table_content))))


def print_syntax(*args: Syntax) -> Source:
    def print_syntax_element(s: Syntax) -> Source:
        return _PRINTERS[type(s)](s)

    seq = Sequence(map(print_syntax_element, [*args]), '\n')

    return print_sequence(seq)
