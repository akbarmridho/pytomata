from lib.preprocess import read_cfg, preprocess
from lib.tokenizer import tokenize, pretty_print
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input
from lib.cyk import cyk

if __name__ == "__main__":
    # Create a list of the terminal from pre-generated terminal text
    terminal_list = []
    terminal_file = open("produced_text/terminals.txt", 'r')
    terminal_lines = terminal_file.readlines()
    for line in terminal_lines:
        terminal_list.append(line.rstrip("\n"))

    # Create a list of the nonterminal from pre-generated nonterminal text
    nonterminal_list = []
    nonterminal_file = open("produced_text/nonterminals.txt", 'r')
    nonterminal_lines = nonterminal_file.readlines()
    for line in nonterminal_lines:
        nonterminal_list.append(line.rstrip("\n"))

    terminal_file.close()
    nonterminal_file.close()

    # Initialize grammar rules
    grammar_rules = read_cfg("produced_text/cnf.txt")

    program_running = True

    DEBUG_DFA = True
    SHOW_TOKENIZED = True

    print("Jika telah dilakukan perubahan pada file CFG, maka disarankan melakukan preprocess untuk meng-update data yang digunakan.")

    is_preprocess = input("Preprocess? (Y/N) ").lower()
    while (is_preprocess != "y" and is_preprocess != "n"):
        print("Jawab dengan benar!")
        is_preprocess = input("Preprocess? (Y/N) ").lower()

    if (is_preprocess == "y"):
        preprocess()

    while (program_running):
        filename = input(
            "Masukkan nama file di folder test yang ingin diuji : ")

        reader = open(f"../test/{filename}")
        original_file = reader.read()
        reader.close()

        original_split = original_file.split("\n")

        tokenized = tokenize(original_file)

        if SHOW_TOKENIZED:
            pretty_print(tokenized)

        tokenized_split = tokenized.split(" ")
        words = str_to_strlang(tokenized)

        ln_total = words.count(NEWLINE)

        decl_error_lines = check_input(declaration_checker, words, DEBUG_DFA)
        words.reverse()
        lced_error_lines = check_input(noitaralced_checker, words, DEBUG_DFA)
        words.reverse()
        arith_error_lines = check_input(
            arith_operation_checker, words, DEBUG_DFA)

        syntax_error_lines = set(
            decl_error_lines + lced_error_lines + arith_error_lines)

        for line_number in syntax_error_lines:
            print(
                f"Found syntax error at line {line_number}: <<{original_split[line_number-1]}>>")
        tokenized_split = tokenized.split(' ')
        print(cyk(tokenized_split, grammar_rules, True))
