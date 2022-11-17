import re
from typing import List, Callable
from .string import symbols_regexp_grouped, symbols_regexp_replacement, symbols_regexp_replacement_val, COMMENT, STRING, VARIABLE, INVALID_VARIABLE, NUMBER, ELSE_IF, ELSE_IF_NL  # type: ignore

Pipe = Callable[[str], str]


def match_relator(match: re.Match, replaceable: List[str]) -> str:
    for i in range(len(replaceable)):
        if match.group(i+1) is not None:
            return replaceable[i]

    return "__error__"


pipeline: List[Pipe] = [
    lambda src: re.sub(symbols_regexp_grouped, lambda x: match_relator(
        x, symbols_regexp_replacement), src),  # add whitespace on symbol
    lambda src: re.sub(COMMENT.pattern, "", src),  # delete string comment
    # change variable named number or string to variable
    lambda src: re.sub(r'^number$|^string$', VARIABLE.value, src),
    lambda src: re.sub(STRING.pattern, STRING.value, src),  # parse string
    # parse variable
    lambda src: re.sub(VARIABLE.pattern, VARIABLE.value, src),
    # parse invalid variable
    lambda src: re.sub(INVALID_VARIABLE.pattern, INVALID_VARIABLE.value, src),
    # parse number
    lambda src: re.sub(NUMBER.pattern, NUMBER.value, src),
    lambda src: re.sub(ELSE_IF.pattern, ELSE_IF.value, src),
    lambda src: re.sub(ELSE_IF_NL.pattern, ELSE_IF_NL.value, src),
    # replace symbols
    lambda src: re.sub(symbols_regexp_grouped, lambda x: match_relator(
        x, symbols_regexp_replacement_val), src)
]


def tokenize(source_code: str) -> str:
    global pipeline

    current_str = source_code

    for pipe in pipeline:
        current_str = pipe(current_str)

    return current_str
