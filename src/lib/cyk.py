from itertools import product


def multiply_cell(list_1, list_2):
    return product(list_1, list_2)


def producer_of(term, cnf):
    producer_list = []
    for rhs, lhs in cnf.items():
        if term in lhs:
            producer_list.append(rhs)
    return producer_list


def print_table(table):
    table_height = len(table)
    for i in range(table_height - 1, -1, -1):
        print(f"Row {i}")
        print(table[i])
        print("\n")


def cyk(string, cnf, reverse_cnf, debug=False, hard_debug=False):

    n = len(string)

    if debug:
        print(n)

    table = [[[] for j in range(n)] for i in range(n)]

    for j in range(n):
        table[0][j] = producer_of([string[j]], cnf)

    for i in range(1, n):
        for j in range(0, n-i):
            for k in range(0, i):
                mul_result_list = multiply_cell(
                    table[k][j], table[i-k-1][j+k+1])
                if (hard_debug):
                    print(f"{i} {j}")
                    print("Operator")
                    print(k, j)
                    print(table[k][j])
                    print(i-k-1, j+k+1)
                    print(table[i-k-1][j+k+1])
                    print("Result")
                    print(mul_result_list)
                for mul_result in mul_result_list:
                    try:
                        table[i][j].extend(reverse_cnf[tuple(mul_result)])
                    except:
                        pass
                if (hard_debug):
                    print("\n")
            if (hard_debug):
                print("Cell Content")
                print(table[i][j])
                print("\n\n")

    if (debug):
        print_table(table)
    if ('SS' in (table[n-1][0])):
        return True
    else:
        return False
