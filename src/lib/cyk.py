def multiply_cell(list_1, list_2):
    result = []
    if (len(list_1) == 0 or len(list_2) == 0):
        return result

    for el_1 in list_1:
        for el_2 in list_2:
            product = []
            product.append(el_1)
            product.append(el_2)
            result.append(product)
    return result


def producer_of(term, cnf):
    producer_list = []
    for rhs, lhs in cnf.items():
        if term in lhs:
            producer_list.append(rhs)
    return producer_list


def cell_pair_to_check(i, j, k):
    return ((k, j), (i-k-1, j+k+1))


def print_table(table):
    table_height = len(table)
    for i in range(table_height - 1, -1, -1):
        print(f"Row {i}")
        print(table[i])
        print("\n")

# print(multiply_cell(['Bruh', 'Bruh2'], ['Bruh2', 'Bruh3']))


def cyk(string, cnf, reverse_cnf, debug=False):

    n = len(string)

    if debug:
        print(n)

    table = [[[] for j in range(n)] for i in range(n)]

    for j in range(n):
        table[0][j] = producer_of([string[j]], cnf)

    for i in range(1, n):
        for j in range(0, n-i):
            cell_content = []
            for k in range(0, i):
                multiplied_1, multiplied_2 = cell_pair_to_check(i, j, k)
                i1, j1 = multiplied_1
                i2, j2 = multiplied_2
                mul_result_list = multiply_cell(table[i1][j1], table[i2][j2])
                if (debug):
                    print(f"{i} {j}")
                    print("Operator")
                    print(multiplied_1)
                    print(table[i1][j1])
                    print(multiplied_2)
                    print(table[i2][j2])
                    print("Result")
                    print(mul_result_list)
                for mul_result in mul_result_list:
                    try:
                        added_list = reverse_cnf[tuple(mul_result)]
                    except (KeyError):
                        added_list = []
                    cell_content = cell_content + added_list
                if (debug):
                    print("\n")
            if (debug):
                print("Cell Content")
                print(cell_content)
                print("\n\n")

            table[i][j] = cell_content

    if (debug):
        print_table(table)
    if ('SS' in (table[n-1][0])):
        return True
    else:
        return False
