import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from src.exceptions import InvalidRuleException


@dataclass
class Rule:
    to_replace: str
    replacement: str
    stop: bool = False

class NAM:
    def __init__(self, filepath: str | Path, skip_whitespaces: bool = True, max_iterations: int = 128):
        self.filepath = filepath
        self.skip_whitespaces = skip_whitespaces
        self.rules: list[Rule] = []
        self.logger = logging.getLogger(__name__)
        self.max_iterations = max_iterations

    def parse_file(self):
        filepath = Path(self.filepath)
        filepath = filepath.expanduser()
        self.logger.debug(f"Opening file {filepath}")
        with open(filepath, "r") as f:
            for ind, line in enumerate(f.readlines(), start = 1):
                self.logger.debug(f"{ind}. {line}")
                if len(line.strip()) == 0:
                    continue
                if self.skip_whitespaces:
                    line = line.replace(" ", "")

                count_sep = line.count("->")
                if count_sep!=1:
                    raise InvalidRuleException(f"Found {count_sep} '->' in {line}", ind)

                to_replace, replacement = line.split("->")
                replacement = replacement.replace("\n", "")
                stop = False
                if replacement[0]==".":
                    stop = True
                    replacement = replacement[1:]

                if to_replace == replacement:
                    raise InvalidRuleException(f"Replacement '{line}' is not allowed: cannot replace with itself", ind)

                rule = Rule(to_replace, replacement, stop)
                self.logger.debug(f"Adding {rule}")
                self.rules.append(rule)

    def apply(self, line: str):
        iters = 0
        while iters<self.max_iterations:
            for rule in self.rules:
                to_replace = rule.to_replace
                replacement = rule.replacement
                stop_ = rule.stop
                ind = line.find(to_replace)
                if ind == -1:
                    continue
                line = line.replace(to_replace, replacement, 1)
                self.logger.debug(f"Applying {rule}")
                self.logger.debug(f"Result: {line}")
                stop = stop_
                break
            else:
                self.logger.warning(f"Could not apply any rules for {line}")
                break
            if stop:
                break
            iters+=1

        if iters>=self.max_iterations:
            self.logger.warning(f"Maximum number of iterations reached({self.max_iterations}), stopping iterations")
        return line

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    nam = NAM("../rules.txt", skip_whitespaces=True)
    nam.parse_file()
    res = nam.apply("111")
    print(res)