from lib.preprocess import read_cfg, preprocess, read_reverse_cnf
from lib.tokenizer import tokenize, pretty_print
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input, conditional_checker
from lib.cyk import cyk
import time

if __name__ == "__main__":
    # Initialize program running mode.
    PROGRAM_RUNNING = True

    is_debug = input("Activate debug mode? (Y/N) ").lower()
    while (is_debug != "y" and is_debug != "n"):
        print("Jawab dengan benar!")
        is_debug = input("Activate debug mode? (Y/N) ").lower()
    debug_active = is_debug == "y"

    is_hard_debug = "n"
    if (debug_active):
        is_hard_debug = input("Activate hardcore debug mode? (Y/N) ").lower()
        while (is_hard_debug != "y" and is_hard_debug != "n"):
            print("Jawab dengan benar!")
            is_hard_debug = input(
                "Activate hardcore debug mode? (Y/N) ").lower()

    hard_debug_active = is_hard_debug == "y"

    DEBUG_DFA = debug_active
    DEBUG_CYK = debug_active
    SHOW_TOKENIZED = debug_active
    DEBUG_CYK_HARD = hard_debug_active

    print("")

    # Initialize grammars
    print("Jika telah dilakukan perubahan pada file CFG, maka disarankan melakukan preprocess untuk memperbaharui grammar yang digunakan.")
    is_preprocess = input("Preprocess? (Y/N) ").lower()
    while (is_preprocess != "y" and is_preprocess != "n"):
        print("Jawab dengan benar!")
        is_preprocess = input("Preprocess? (Y/N) ").lower()

    if (is_preprocess == "y"):
        preprocess()

    grammar_rules = read_cfg("produced_text/cnf.txt")
    reverse_cnf = read_reverse_cnf("produced_text/reverse_cnf.txt")

    # Memulai keberjalanan program
    while (PROGRAM_RUNNING):

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
        print("Parsing your Javascript file...")
        parse_start = time.perf_counter()

        # Tokenisasi file yang dimasukkan
        original_split = original_file.split("\n")

        tokenized = tokenize(original_file)

        tokenized_split = tokenized.split(" ")
        words = str_to_strlang(tokenized)

        ln_total = words.count(NEWLINE)

        # Pengecekan file dengan menggunakan DFA
        decl_error_lines = check_input(declaration_checker, words, DEBUG_DFA)
        words.reverse()

        lced_error_lines = check_input(noitaralced_checker, words, DEBUG_DFA)
        words.reverse()

        arith_error_lines = check_input(
            arith_operation_checker, words, DEBUG_DFA)

        conditional_error_lines = check_input(
            conditional_checker, words, DEBUG_DFA)

        # Agregasi semua error line dari DFA
        syntax_error_lines = set(
            decl_error_lines + lced_error_lines + arith_error_lines + conditional_error_lines)

        dfa_result = syntax_error_lines.__len__() == 0

        tokenized_split_with_nl = tokenized.split(' ')
        tokenized_split = []

        for each in tokenized_split_with_nl:
            if each != "nl":
                tokenized_split.append(each)

        # Parsing dengan menggunakan algoritma CYK
        cyk_result = cyk(tokenized_split, grammar_rules,
                         reverse_cnf, DEBUG_CYK, DEBUG_CYK_HARD)

        result = cyk_result

        # Cetak hasil debugging yang sesuai
        if DEBUG_DFA:
            print(f"DFA Result : {dfa_result}")
            print(f"CYK Result : {cyk_result}")

        if SHOW_TOKENIZED:
            pretty_print(tokenized)

        # Cetak kesalahan yang ditemukan oleh DFA
        if not dfa_result and not result:
            print("SYNTAX ERROR AT DFA")
            for line_number in syntax_error_lines:
                print(
                    f"Found syntax error at line {line_number}: <<{original_split[line_number-1]}>>")

        parse_end = time.perf_counter()
        if (result):
            print(f"File {filename} benar secara syntax")
        else:
            print(f"File {filename} salah secara syntax")
        print(
            f"Parsing selesai dalam {round(parse_end - parse_start, 3)} detik\n")
        PROGRAM_RUNNING = input(
            "Ketik 0 untuk keluar : ") != "0"
        # if (continue_program == "0"):
        #     PROGRAM_RUNNING = False
