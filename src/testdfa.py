from lib.tokenizer import tokenize, pretty_print
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input

tokenized: str

with open('2.js') as f:
    tokenized = tokenize(f.read())

pretty_print(tokenized)

word = str_to_strlang(tokenized)

ln_total = word.count(NEWLINE)

print(f"DECLARATION CHECKER")

print("DECLARATION CHECKER BEGIN\n")
decl_error_lines = check_input(declaration_checker, word, True)

for line in decl_error_lines:
    print(f"Invalid variable declaration at line {line}")

print("DECLARATION CHECKER END\n")

word.reverse()

print("REVERSE DECLARATION CHEKER BEGIN\n")

lced_error_lines = check_input(noitaralced_checker, word, True)

for line in lced_error_lines:
    print(f"Invalid variable naming at line {ln_total-line+2}")

print("REVERSE DECLARATION CHECKER END\n")

word.reverse()

print("ARITHMETIC OPERATION CHECKER BEGIN\n")

arith_error_lines = check_input(arith_operation_checker, word, True)

for line in arith_error_lines:
    print(f"Invalid arithmetic operation at line {line}")

print("ARITHMETIC OPERATION CHECKER END\n")
