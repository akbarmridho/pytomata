from lib.preprocess import read_cfg, preprocess, read_reverse_cnf
from lib.tokenizer import tokenize
from lib.string import str_to_strlang, NEWLINE
from lib.dfa import declaration_checker, noitaralced_checker, arith_operation_checker, check_input, conditional_checker
from lib.cyk import cyk
from lib.path import get_files
import os
import time

if __name__ == "__main__":
    preprocess()

    grammar_rules = read_cfg("produced_text/cnf.txt")
    reverse_cnf = read_reverse_cnf("produced_text/reverse_cnf.txt")

    total_count = 0
    pass_count = 0

    for filepath in get_files("../test"):

        filename = filepath.split(os.sep)[-1]
        print(f"Checking file {filename}: ", end="", flush=True)

        if filename[0] == 's':
            print(" skipping")
            continue

        reader = open(filepath)
        original_file = reader.read()
        reader.close()

        tic = time.perf_counter()
        original_split = original_file.split("\n")

        tokenized = tokenize(original_file)

        tokenized_split = tokenized.split(" ")
        words = str_to_strlang(tokenized)

        ln_total = words.count(NEWLINE)

        decl_error_lines = check_input(declaration_checker, words, False)
        words.reverse()
        lced_error_lines = check_input(noitaralced_checker, words, False)
        words.reverse()
        arith_error_lines = check_input(
            arith_operation_checker, words, False)

        conditional_error_lines = check_input(
            conditional_checker, words, False)

        syntax_error_lines = set(
            decl_error_lines + lced_error_lines + arith_error_lines + conditional_error_lines)

        dfa_result = syntax_error_lines.__len__() == 0

        tokenized_split_with_nl = tokenized.split(' ')
        tokenized_split = []

        for each in tokenized_split_with_nl:
            if each != "nl":
                tokenized_split.append(each)
        if (len(tokenized_split) == 0):
            cyk_result = True
        else:
            cyk_result = cyk(tokenized_split, reverse_cnf, False)

        if not dfa_result:
            if cyk_result:
                result = True
            else:
                result = False
        else:
            result = dfa_result and cyk_result

        toc = time.perf_counter()

        res = "valid" if result else "invalid"
        expect = "valid" if filename[0] == 't' else "invalid"
        is_pass = "PASS" if res == expect else "FAIL"

        if toc-tic < 1:
            parse_time = f"{(toc-tic)*1000:.2f}ms"
        else:
            parse_time = f"{toc-tic:.2f}s"

        print(
            f"expected {expect} got {res} parsed in {parse_time} {is_pass}")

        total_count += 1

        if res == expect:
            pass_count += 1

    print(f"TEST RESULT: corrent {pass_count} out of {total_count}")
