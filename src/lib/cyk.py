from itertools import product


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


def cyk(string, reverse_cnf, debug=False, hard_debug=False):
    n = len(string)

    if (n == 0):
        return True

    if debug:
        print(n)

    table = [[set([]) for j in range(n)] for i in range(n)]
    for j in range(n):
        try:
            table[0][j] = reverse_cnf[tuple([string[j]])]
        except:
            table[0][j] = set([])

    for i in range(1, n):
        for j in range(0, n-i):
            for k in range(0, i):
                mul_result_list = set(product(
                    table[k][j], table[i-k-1][j+k+1]))
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
                        table[i][j] = table[i][j].union(
                            reverse_cnf[tuple(mul_result)])
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
