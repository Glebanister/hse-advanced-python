#!/usr/bin/env python3

import argparse
import sys
import traceback

from pathlib import Path

import ast_visualizer


def visualize_with_args(args: argparse.Namespace):
    output_file_path = None if args.output is None else Path(args.output)
    if args.file is not None:
        ast_visualizer.visualize_from_file(Path(args.file), output_file_path, args.no_show)
    else:
        all_input = sys.stdin.read()
        ast_visualizer.visualize_from_source(all_input, output_file_path, args.no_show)


def main():
    arg_parser = argparse.ArgumentParser(description='Python code visualizer')
    arg_parser.add_argument(help='Specify path to the sources file'
                            'If no path is specified, stdin will be used',
                            nargs='?',
                            dest='file')
    arg_parser.add_argument('--output',
                            help='Specify output filename to store graph.'
                            'Graph only will be shown by default')
    arg_parser.add_argument('--with-traceback',
                            help='Print error with traceback',
                            action='store_true')
    arg_parser.add_argument('--no-show',
                            help='Do not show graph',
                            action='store_true')
    try:
        args = arg_parser.parse_args()
        visualize_with_args(args)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        if args.with_traceback:
            traceback.print_exc()


if __name__ == '__main__':
    main()
