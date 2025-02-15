import argparse
from typing import Iterable, Protocol, Sequence, Union


from runner.matching.script_selectors import parse_selector_list


class Command(Protocol):
    command: str
    selector: list[str]
    dry: bool


def add_selector(p: argparse.ArgumentParser):
    p.add_argument(
        "selector",
        nargs="+",
        help="a multipart selector for the installation scripts to run.",
    )


class Cli:
    def __init__(self):
        root_parser = argparse.ArgumentParser(description="Perdido setup script runner")
        subparsers = root_parser.add_subparsers(
            title="command", required=True, dest="command"
        )

        run = subparsers.add_parser(
            "run",
            help="run one or more installation scripts",
        )

        run.add_argument(
            "-D",
            "--dry",
            dest="dry",
            action="store_true",
            help="don't actually run the scripts",
            required=False,
        )
        add_selector(run)
        list = subparsers.add_parser("list", help="list installation scripts")
        add_selector(list)
        printing = subparsers.add_parser("print", help="print installation scripts")
        add_selector(printing)

        self._parser = root_parser

    def parse(self, args: Union[Sequence[str], None] = None) -> Command:
        args_result = self._parser.parse_args(args)
        if hasattr(args_result, "rule"):
            args_result.rule = parse_selector_list(args_result.rule)
        return args_result  # type: ignore
