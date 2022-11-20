from typing import List, Dict


class StringLanguage:
    pattern: str
    value: str

    def __init__(self, pattern: str, value: str):
        self.pattern = pattern
        self.value = value

    @property
    def exact_match(self):
        splitted = self.pattern.split('|')

        for i in range(len(splitted)):
            splitted[i] = f"^{splitted[i]}$"

        return '|'.join(splitted)


"""Reserved Words
"""
BREAK = StringLanguage(value="break", pattern="break")
CONST = StringLanguage(value="const", pattern="const")
CASE = StringLanguage(value="case", pattern="case")
CATCH = StringLanguage(value="catch", pattern="catch")
CONTINUE = StringLanguage(value="continue", pattern="continue")
DEFAULT = StringLanguage(value="default", pattern="default")
DELETE = StringLanguage(value="delete", pattern="delete")
ELSE = StringLanguage(value="else", pattern=r"else(?!\s+if)")
ELSE_IF = StringLanguage(value="elif", pattern=r"else\s+if")
FALSE = StringLanguage(value="false", pattern="false")
FINALLY = StringLanguage(value="finally", pattern="finally")
FOR = StringLanguage(value="for", pattern="for")
FUNCTION = StringLanguage(value="function", pattern="function")
IF = StringLanguage(value="if", pattern=r"(?!else\s+)if")
LET = StringLanguage(value="let", pattern="let")
NULL = StringLanguage(value="null", pattern="null")
RETURN = StringLanguage(value="return", pattern="return")
SWITCH = StringLanguage(value="switch", pattern="switch")
THROW = StringLanguage(value="throw", pattern="throw")
TRUE = StringLanguage(value="true", pattern="true")
TRY = StringLanguage(value="try", pattern="try")
VAR = StringLanguage(value="var", pattern="var")
WHILE = StringLanguage(value="while", pattern="while")

reserved_words: List[StringLanguage] = [
    ELSE_IF,
    BREAK,
    CONST,
    CASE,
    CATCH,
    CONTINUE,
    DEFAULT,
    DELETE,
    ELSE,
    FALSE,
    FINALLY,
    FOR,
    FUNCTION,
    IF,
    LET,
    NULL,
    RETURN,
    SWITCH,
    THROW,
    TRUE,
    TRY,
    VAR,
    WHILE
]

reserved_words_regexp = r"|".join([word.pattern for word in reserved_words])

"""Symbols
"""
ASSIGN = StringLanguage(value="assign", pattern="=")
AND = StringLanguage(value="and", pattern="&&")
BAND = StringLanguage(value="band", pattern="&")
BOR = StringLanguage(value="bor", pattern="\|")
COLON = StringLanguage(value="colon", pattern=":")
COMMA = StringLanguage(value="comma", pattern=",")
CBRACKETL = StringLanguage(value="cbraketl", pattern="{")
CBRACKETR = StringLanguage(value="cbracketr", pattern="}")
DIVIDE = StringLanguage(value="divide", pattern=r"/")
DIVIDEEQ = StringLanguage(value="divideeq", pattern=r"\\=")
EQUAL = StringLanguage(value="equal", pattern="===|==")
GREATER = StringLanguage(value="greater", pattern=">")
GREATEREQ = StringLanguage(value="greatereq", pattern=">=")
DECREMENT = StringLanguage(value="dec", pattern=r"--")
INCREMENT = StringLanguage(value="inc", pattern=r"\+\+")
LESS = StringLanguage(value="less", pattern="<")
LESSEQ = StringLanguage(value="lesseq", pattern="<=")
NEWLINE = StringLanguage(value="nl", pattern=r"\n|\r\n|\r")
NEQUAL = StringLanguage(value="nequal", pattern="!==|!=")
SEMICOLON = StringLanguage(value="semicolon", pattern=";")
PLUS = StringLanguage(value="plus", pattern=r"\+")
PLUSEQ = StringLanguage(value="pluseq", pattern=r"\+=")
POW = StringLanguage(value="pow", pattern="\*\*")
POWEQ = StringLanguage(value="poweq", pattern="\*\*=")
MULTIPLY = StringLanguage(value="multiply", pattern=r"\*")
MULTIPLYEQ = StringLanguage(value="multiplyeq", pattern=r"\*=")
MINUS = StringLanguage(value="minus", pattern=r"-")
MINUSEQ = StringLanguage(value="minuseq", pattern=r"-=")
MODULO = StringLanguage(value="mod", pattern=r"%")
MODULOEQ = StringLanguage(value="modeq", pattern="%=")
OR = StringLanguage(value="or", pattern=r"\|\|")
QMARK = StringLanguage(value="qmark", pattern="\?")
RBRACKETL = StringLanguage(value="rbracketl", pattern=r"\(")
RBRACKETR = StringLanguage(value="rbracketr", pattern=r"\)")
SBRACKETL = StringLanguage(value="sbracketl", pattern=r"\[")
SBRACKETR = StringLanguage(value="sbracketr", pattern=r"\]")
SHIFT = StringLanguage(value="shift", pattern=">>|<<|>>>")
XOR = StringLanguage(value="xor", pattern="\^")


symbols: List[StringLanguage] = [
    DIVIDEEQ,
    SHIFT,
    GREATEREQ,
    LESSEQ,
    PLUSEQ,
    MULTIPLYEQ,
    MINUSEQ,
    POWEQ,
    MODULOEQ,
    DECREMENT,
    INCREMENT,
    EQUAL,
    NEQUAL,
    POW,
    AND,
    BAND,
    COLON,
    COMMA,
    CBRACKETL,
    CBRACKETR,
    DIVIDE,
    GREATER,
    LESS,
    NEWLINE,
    SEMICOLON,
    PLUS,
    MULTIPLY,
    MINUS,
    MODULO,
    OR,
    BOR,
    QMARK,
    XOR,
    ASSIGN,
    RBRACKETL,
    RBRACKETR,
    SBRACKETL,
    SBRACKETR
]  # urutan harus sesuai prioritas

symbols_regexp = "|".join(symbol.pattern for symbol in symbols)

"""Convertable
"""
STRING = StringLanguage(
    value="string", pattern=r"|".join(['"[^"\n\r]*"|"[^"]*[\r\n]', r"'[^'\n\r]*'|'[^']*[\r\n]", r"`[^`]*`|`[^`]*$"]))  # todo: handle ketika ada ", ', atau ` di dalam string`
NUMBER = StringLanguage(value="number", pattern=r"\d+\.?\d*|\.\d+")
COMMENT = StringLanguage(
    value="", pattern=r"\/\*[^\*\/]*\*\/|\*[^\*\/]*$|\/\/.*[\r\n]")

INVALID_VARIABLE = StringLanguage(
    value="number variable", pattern=r"[0-9]+[a-zA-Z_]\w*")
VARIABLE = StringLanguage(
    value="variable", pattern=rf"\b(?!{reserved_words_regexp}|variable|string\b)[a-zA-Z_]+[a-zA-Z0-9_]*")

language = [STRING, NUMBER, VARIABLE]
language.extend(reserved_words)
language.extend(symbols)

language_dict: Dict[str, StringLanguage] = {}

for lang in language:
    language_dict[lang.value] = lang
