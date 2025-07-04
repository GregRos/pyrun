from dataclasses import dataclass
from pathlib import Path
from pyrun._exec.bash_exec_prefix import BashPrefixExecutor
from pyrun._scripts.indexed import (
    is_valid_script,
    must_parse_indexed,
    try_parse_indexed,
)
from pyrun._scripts.pretty_print import pretty_print_lines
from pyrun._scripts.runnable import Runnable


@dataclass
class Script(Runnable):
    path: Path
    name: str

    @staticmethod
    def is_valid_indexed(path: Path):
        return try_parse_indexed(path.stem) is not None and is_valid_script(path)

    @classmethod
    def from_indexed_path(cls, parent: Runnable, path: Path):
        if not path.is_file():
            raise Exception(f"Expected a file, got {path}")
        if not cls.is_valid_indexed(path):
            raise Exception(f"Invalid indexed path: {path}")
        [pos, str] = must_parse_indexed(path.stem)
        return Script(pos, str, parent, path)

    @staticmethod
    def from_named(parent: Runnable | None, path: Path, name: str | None = None):
        name = name or path.stem
        return Script(None, name, parent, path)

    def __repr__(self) -> str:
        return f"{self:line}"

    @property
    def contents(self):
        return self.path.read_text()

    def __len__(self):
        return len(self.contents)

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "full":
                lines = pretty_print_lines(self.address, self.contents)
                return lines
            case "child":
                return f"{self.name}[{len(self)}]!"
            case "line":
                return f"{self.address}[{len(self)}]!"
            case "short":
                return f"{self.caption}!"
            case "address":
                return f"{self.address}!"
            case _:
                raise ValueError(f"Unknown format spec: {format_spec}")

    def __str__(self) -> str:
        if self.pos is not None:
            return f"{self.pos:02d}:{self.name}"
        return self.name

    def run(self, executor: BashPrefixExecutor):
        cwd = self.path.parent
        executor.must_exec(self.path, cwd, self.address)
        # code to exec
