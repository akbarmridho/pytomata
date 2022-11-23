from lib.preprocess import read_cfg, preprocess, read_reverse_cnf
from lib.tokenizer import tokenize, pretty_print
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input, conditional_checker
from lib.cyk import cyk
from lib.path import get_files
import os
import time

if __name__ == "__main__":
    # Initialize grammar rules
    DEBUG_DFA = False
    DEBUG_DFA = False
    DEBUG_CYK = False

    preprocess()

    grammar_rules = read_cfg("produced_text/cnf.txt")
    reverse_cnf = read_reverse_cnf("produced_text/reverse_cnf.txt")

    total_count = 0
    pass_count = 0

    for filepath in get_files("../test"):

        filename = filepath.split(os.sep)[-1]
        print(f"Checking file {filename}: ", end="")

        reader = open(filepath)
        original_file = reader.read()
        reader.close()

        tic = time.perf_counter()
        original_split = original_file.split("\n")

        tokenized = tokenize(original_file)

        tokenized_split = tokenized.split(" ")
        words = str_to_strlang(tokenized)

        ln_total = words.count(NEWLINE)

        decl_error_lines = check_input(declaration_checker, words, DEBUG_DFA)
        words.reverse()
        lced_error_lines = check_input(noitaralced_checker, words, DEBUG_DFA)
        words.reverse()
        arith_error_lines = check_input(
            arith_operation_checker, words, DEBUG_DFA)

        conditional_error_lines = check_input(
            conditional_checker, words, DEBUG_DFA)

        syntax_error_lines = set(
            decl_error_lines + lced_error_lines + arith_error_lines + conditional_error_lines)

        result = syntax_error_lines.__len__() == 0

        if result:
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

        res = "valid" if result else "invalid"
        expect = "valid" if filename[0] == 't' else "invalid"
        is_pass = "PASS" if res == expect else "FAIL"

        print(
            f"expected {expect} got {res} parsed in {(toc-tic)*1000:.2f}ms {is_pass}")

        total_count += 1

        if res == expect:
            pass_count += 1

    print(f"TEST RESULT: corrent {pass_count} out of {total_count}")
