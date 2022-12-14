import re
from typing import List, Callable
from math import log10, ceil
from .string import symbols_regexp, COMMENT, STRING, VARIABLE, INVALID_VARIABLE, NUMBER, ELSE_IF, symbols  # type: ignore

Pipe = Callable[[str], str]


def comment_sub(match: re.Match):
    matched: str = match.group(0)

    if matched.startswith(r"//"):
        return "\n"
    else:
        nl_count = matched.count('\n')
        if nl_count == 0:
            return ""
        else:
            return nl_count*"\n"


def elif_sub(match: re.Match):
    global ELSE_IF
    matched: str = match.group(0)

    nl_count = matched.count('\n')

    if nl_count == 0:
        return ELSE_IF.value
    else:
        return ELSE_IF.value + nl_count*"\n"


def pipe_debug(src: str, pattern: str, replacement: str) -> str:
    return re.sub(pattern, replacement, src)


pipeline: List[Pipe] = [
    # delete escaped charapter
    lambda src: re.sub("|".join([r"\\'", r'\\"', r'\\\\']), "", src),
    # delete string comment
    lambda src: re.sub(COMMENT.pattern, lambda x: comment_sub(x), src),
    # add whitespace on symbol
    lambda src: re.sub(
        symbols_regexp, lambda x: rf" {x.group(0)} ", src),  # type: ignore
    # change variable named number or string to variable
    lambda src: re.sub(r'^number$|^string$', VARIABLE.value, src),
    # parse string 3 time to ensure validity (handle edge case like: ' "" ')
    lambda src: re.sub(STRING.pattern, STRING.value, src),
    lambda src: re.sub(STRING.pattern, STRING.value, src),
    lambda src: re.sub(STRING.pattern, STRING.value, src),
    # parse variable
    lambda src: re.sub(VARIABLE.pattern, VARIABLE.value, src),
    # parse invalid variable
    lambda src: re.sub(INVALID_VARIABLE.pattern, INVALID_VARIABLE.value, src),
    # parse number
    lambda src: re.sub(NUMBER.pattern, f" {NUMBER.value} ", src),
    lambda src: re.sub(ELSE_IF.pattern, lambda x: elif_sub(x), src),
    # # replace symbols
    *[
        (lambda sym:
         lambda src: pipe_debug(src, sym.pattern, sym.value))(symbol)
        for symbol in symbols],
    # delete unnecesarry whitespace
    lambda src: re.sub("\s+", " ", src),
    # handle nested object property access
    lambda src: re.sub("variable( dot variable)*", "variable", src)
]


def tokenize(source_code: str) -> str:
    global pipeline

    current_str = source_code

    for pipe in pipeline:
        current_str = pipe(current_str)

    return current_str.strip()


def pretty_print(string: str):
    splitted = string.replace("nl", "nl\n").split("\n")
    pad = ceil(log10(splitted.__len__()))
    for i in range(splitted.__len__()):
        no = str(i+1) + " "*(pad-str(i).__len__())
        print(f"{no}: {splitted[i].strip()}")
