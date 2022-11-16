from typing import List, Callable
from .string import symbols_regexp_grouped, symbols_regexp_replacement, COMMENT  # type: ignore
import re

Pipe = Callable[[str], str]


def match_relator(match: re.Match, replaceable: List[str]) -> str:
    for i in range(len(replaceable)):
        if match.group(i+1) is not None:
            return replaceable[i]

    return "__error__"


pipeline: List[Pipe] = [
    lambda src: re.sub(symbols_regexp_grouped, lambda x: match_relator(
        x, symbols_regexp_replacement), src),  # add whitespace on symbol
    lambda src: re.sub(COMMENT.pattern, "", src)  # hapus string comment
]


def tokenize(source_code: str) -> str:
    global pipeline

    current_str = source_code

    for pipe in pipeline:
        current_str = pipe(current_str)

    return current_str
