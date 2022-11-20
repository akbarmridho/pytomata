from lib.cfgtocnf import read_cfg

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
