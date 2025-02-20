from time import sleep
from termcolor import colored
from pyrun._exec.bash_exec_prefix import BashPrefixExecutor
from pyrun._scripts.runnable import Runnable
from pyrun._scripts.script import Script


class MatchedSet(Runnable):

    def __init__(self, multipart: list[str], kids: list[Runnable]):
        super().__init__(
            pos=None,
            name=None,
            parent=None,
        )
        self.query = ", ".join(multipart)
        self.kids = kids

    def run(self, executor: BashPrefixExecutor):
        for kid in self.kids:
            kid.run(executor)
        sleep(0.1)
        print(
            colored(f"      ↑ DONE ↑      ", color="white", on_color="on_light_green"),
            "\n",
        )

    def __len__(self) -> int:
        from pyrun._scripts.pack import Pack

        count = 0
        for x in self.kids:
            match x:
                case Pack():
                    count += len(x)
                case Script():
                    count += 1
                case _:
                    raise ValueError(f"Unknown type: {type(x)}")
        return count

    def __iter__(self):
        return iter(self.kids)

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "full":
                texts = []
                for kid in self.kids:
                    texts.append(f"{kid:full}")
                return "\n".join(texts)
            case "summary":
                lines = []
                for script in self:
                    lines.append(f"{script:short}")
                return "\n".join(lines)
            case "child":
                return f"{self.query}[{len(self)}]!"
            case "line":
                return f"{self.query}[{len(self)}]!"
            case "short":
                return f"{self.query}!"
            case "address":
                return f"{self.query}!"
            case _:
                raise ValueError(f"Unknown format spec: {format_spec}")

    def __repr__(self) -> str:
        return self.__format__("line")

    def __str__(self) -> str:
        return self.__format__("short")
