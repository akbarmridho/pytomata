from lib.preprocess import read_cfg, preprocess, read_reverse_cnf
from lib.tokenizer import tokenize, pretty_print
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input
from lib.cyk import cyk
import time

if __name__ == "__main__":
    # Initialize grammar rules
    program_running = True

    DEBUG_DFA = True
    SHOW_TOKENIZED = True

    is_debug = input("Activate debug mode? (Y/N) ").lower()
    while (is_debug != "y" and is_debug != "n"):
        print("Jawab dengan benar!")
        is_debug = input("Preprocess? (Y/N) ").lower()

    debug_active = is_debug == "y"

    DEBUG_DFA = debug_active
    DEBUG_CYK = debug_active

    print("Jika telah dilakukan perubahan pada file CFG, maka disarankan melakukan preprocess untuk meng-update data yang digunakan.")

    is_preprocess = input("Preprocess? (Y/N) ").lower()
    while (is_preprocess != "y" and is_preprocess != "n"):
        print("Jawab dengan benar!")
        is_preprocess = input("Preprocess? (Y/N) ").lower()

    if (is_preprocess == "y"):
        preprocess()

    grammar_rules = read_cfg("produced_text/cnf.txt")
    reverse_cnf = read_reverse_cnf("produced_text/reverse_cnf.txt")

    # print(reverse_cnf)

    while (program_running):

        file_valid = False
        while (not file_valid):
            try:
                filename = input(
                    "Masukkan nama file di folder test yang ingin diuji : ")
                reader = open(f"../test/{filename}")
                original_file = reader.read()
                reader.close()
                file_valid = True
            except (FileNotFoundError):
                print("File tidak ditemukan.")

        tic = time.perf_counter()
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

        if syntax_error_lines.__len__() != 0:
            print("SYNTAX ERROR AT DFA")

        for line_number in syntax_error_lines:
            print(
                f"Found syntax error at line {line_number}: <<{original_split[line_number-1]}>>")

        if syntax_error_lines.__len__() == 0:
            tokenized_split_with_nl = tokenized.split(' ')
            tokenized_split = []

            for each in tokenized_split_with_nl:
                if each != "nl":
                    tokenized_split.append(each)
            if (len(tokenized_split) == 0):
                result = True
            else:
                result = cyk(tokenized_split, grammar_rules,
                             reverse_cnf, DEBUG_CYK)

        toc = time.perf_counter()
        if (result):
            print(f"File {filename} benar secara syntax")
        else:
            print(f"File {filename} salah secara syntax")
        print(f"File di-parse dalam {toc - tic} detik")
