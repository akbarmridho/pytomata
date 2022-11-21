def read_cfg(file):
    cfg = {}
    lines = open(file, 'r').readlines()
    for line in lines:
        rules = line.rstrip('\n').split('->')
        rules[0] = rules[0].rstrip(' ')
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
            if val == start_symbol:
                cfg['SS'] = start_symbol
                found_start = True
                break
        if(found_start):break
    
    # 2. Remove Unit Production
    unit_production = []
    for key in cfg:
        for val in cfg[key]:
            if (len(val)==1 and not val[0].islower()):
                unit_production.append(key)
    while(len(unit_production)!=0):
        for val in cfg[unit_production[0]]:
            if(len(val)==1 and not val[0].islower()):
                temp = val[0]
                cfg[unit_production[0]].remove(val)
                cfg[unit_production[0]]+=(cfg[temp])
                for val in cfg[temp]:
                    if(len(val)==1 and not val[0].islower()):
                        unit_production.append(temp)
        unit_production.pop(0)
    # for key in cfg:
    #     print (key)
    #     print(cfg[key])
    # 3. Replace each production A-> B1 ... Bn where n>2,with A-> B1C where C -> B2...Bn
    new_cnf = {}
    for key in cfg:
        idx = 0
        for vals in cfg[key]:
            while(len(vals)>2):
                new_rule = vals[0:2]
                print([new_rule])
                vals = vals[2:]
                found = False
                # Traverse dict to check if new_rule is already a production
                for key_ctr in new_cnf:
                    if (new_cnf[key_ctr]==[new_rule]):
                        new_key = key_ctr
                        found = True
                        break
                # if not, make new rulegit
                if(not found):
                    new_key = key+str(idx)
                    new_cnf[new_key] = [new_rule]
                vals.insert(0,new_key)
                idx+=1
            if key not in new_cnf:
                productions = []
                productions.append(vals)
                new_cnf[key] = productions
            else:
                new_cnf[key].append(vals)
    return new_cnf

def write_cnf(cnf):
    file = open ('cnf.txt','w')
    for key in cnf:
        for vals in cnf[key]:
            file.write(key + ' -> ')
            for val in vals:
                file.write(val+' ')
            file.write('\n')
    file.close()

if __name__ == "__main__":
    cnf = to_cnf(read_cfg("cfg.txt"))
    write_cnf(cnf)