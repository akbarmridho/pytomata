from .string import language_dict
from typing import Dict, List


def read_cfg(file):
    cfg = {}
    lines = open(file, 'r').readlines()
    for line in lines:
        rules = line.rstrip('\n').split('->')
        rules[0] = rules[0].rstrip(' ')
        if (len(rules) > 1):
            if rules[0] not in cfg.keys():
                productions = []
                productions.append(rules[1].split())
                cfg[rules[0]] = productions
            else:
                cfg[rules[0]].append(rules[1].split())
    return cfg


def to_cnf(cfg):
    # 1. If the Start Symbol S occurs on some right side, create a new Start Symbol S' and a new Production S' -> S
    start_symbol = 'S'
    found_start = False
    for vals in cfg.values():
        for val in vals:
            if start_symbol in val:
                cfg['SS'] = [start_symbol]
                found_start = True
                break
        if (found_start):
            break

    # 2. Remove Unit Production
    unit_production = []
    for key in cfg:
        for val in cfg[key]:
            if (len(val) == 1 and not val[0].islower()):
                unit_production.append(key)
    while (len(unit_production) != 0):
        for val in cfg[unit_production[0]]:
            if (len(val) == 1 and not val[0].islower()):
                temp = val[0]
                cfg[unit_production[0]].remove(val)
                cfg[unit_production[0]] += (cfg[temp])
                for val in cfg[temp]:
                    if (len(val) == 1 and not val[0].islower()):
                        unit_production.append(temp)
                        unit_production.append(unit_production[0])
        unit_production.pop(0)
    # for key in cfg:
    #     print (key)
    #     print(cfg[key])
    # 3. Replace each production A-> B1 ... Bn where n>2,with A-> B1C where C -> B2...Bn
    new_cnf = {}
    for key in cfg:
        idx = 0
        for vals in cfg[key]:
            while (len(vals) > 2):
                new_rule = vals[0:2]
                # print([new_rule])
                vals = vals[2:]
                found = False
                # Traverse dict to check if new_rule is already a production
                for key_ctr in new_cnf:
                    if (new_cnf[key_ctr] == [new_rule]):
                        new_key = key_ctr
                        found = True
                        break
                # if not, make new rulegit
                if (not found):
                    new_key = key+str(idx)
                    new_cnf[new_key] = [new_rule]
                vals.insert(0, new_key)
                idx += 1
            if key not in new_cnf:
                productions = []
                productions.append(vals)
                new_cnf[key] = productions
            else:
                new_cnf[key].append(vals)
    return new_cnf


def produce_term(file):
    global language_dict

    right_side = set([])
    left_side = set([])
    lines = open(file, 'r').readlines()
    for line in lines:
        rules = line.rstrip('\n').split('->')
        if (len(rules) > 1):
            right_side.add(rules[0].strip())
            left_side = left_side.union(set(rules[1].strip().split(' ')))
    left_side = left_side - right_side
    terminal_file = open('produced_text/terminals.txt', 'w')
    nonterminal_file = open('produced_text/nonterminals.txt', 'w')
    for rs in right_side:
        terminal_file.write(rs)
        terminal_file.write('\n')
    for ls in left_side:
        nonterminal_file.write(ls)
        nonterminal_file.write('\n')
    terminal_file.close()
    nonterminal_file.close()


def to_reverse_cnf(cnf):
    reverse_cfg = {}
    for variable, products in cnf.items():
        for product in products:
            product_temp = tuple(product)
            if (not (product_temp in reverse_cfg)):
                reverse_cfg[product_temp] = set([])
            reverse_cfg[product_temp].add(variable)
    return reverse_cfg


def write_cnf(cnf):
    file = open('produced_text/cnf.txt', 'w')
    for key in cnf:
        for vals in cnf[key]:
            file.write(key + ' -> ')
            for val in vals:
                file.write(val+' ')
            file.write('\n')
    file.close()


def write_reverse_cnf(reversed_cnf):
    file = open('produced_text/reverse_cnf.txt', 'w')
    for product, variables in reversed_cnf.items():
        for variable in variables:
            product_to_write = ' '.join(map(str, product))
            file.write(product_to_write + ' <- ' + variable)
            file.write('\n')
    file.close()


def read_reverse_cnf(r_cnf_filename):
    file = open(r_cnf_filename, 'r')
    lines = file.readlines()
    reverse_cnf = {}
    for line in lines:
        unsplit_product, variable = line.rstrip('\n').split(' <- ')
        product = tuple(unsplit_product.split(' '))
        if (not (product in reverse_cnf)):
            reverse_cnf[product] = []
        reverse_cnf[product].append(variable)

    file.close()
    return reverse_cnf


def validate_cnf(cnf: Dict[str, List[List[str]]]):
    terminals: Dict[str, bool] = {}

    for terminal in cnf.keys():
        terminals[terminal] = True

    for key, prod in cnf.items():
        for rule in prod:
            rulestr = f"{key} -> " + " ".join(rule)

            if len(rule) == 2:
                if rule[0] not in terminals:
                    print(
                        f"CNF Validation error on {rulestr}: terminal {rule[0]} could not be found")
                elif rule[1] not in terminals:
                    print(
                        f"CNF Validation error on {rulestr}: terminal {rule[1]} could not be found")
            elif len(rule) == 1:
                if rule[0] not in language_dict:
                    print(
                        f"CNF Validation error on {rulestr}: string {rule[0]} was not found in language")
            else:
                print(
                    f"CNF validation error on {rulestr}: right side length must be one or two")


def preprocess():
    cnf = to_cnf(read_cfg("produced_text/cfg.txt"))
    write_cnf(cnf)
    write_reverse_cnf(to_reverse_cnf(cnf))
    validate_cnf(cnf)
