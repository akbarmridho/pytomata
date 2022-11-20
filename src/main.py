from lib.preprocess import read_cfg, preprocess

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

program_running = True

while (program_running):
    print("Jika telah dilakukan perubahan pada file CFG, maka disarankan melakukan preprocess untuk meng-update data yang digunakan.")
    initial_input_valid = False

    preprocess = input("Preprocess? (Y/N) ").lower()
    while (preprocess != "y" or preprocess != "n"):
        print("Jawab dengan benar!")
        preprocess = input("Preprocess? (Y/N) ").lower()

    if (preprocess == "y"):
        preprocess()

    filename = input("Masukkan nama file di folder test yang ingin diuji : ")
