from .string import *
from typing import List, Dict, TypedDict


class State(TypedDict):
    is_start: bool
    is_final: bool
    name: str


class Transition(TypedDict):
    input_state: State
    result_state: State
    string: StringLanguage


class DFA:
    transitions: Dict[StringLanguage, Dict[State, State]]
    curent_state: State
    initial_state: State
    has_initial: bool = False
    has_final: bool = False

    def __init__(self, transitions: List[Transition]):
        self.transitions = {}

        for transition in transitions:
            string = transition['string']
            state_dict: Dict[State, State]

            if string in self.transitions:
                state_dict = self.transitions[string]
            else:
                state_dict = {}
                self.transitions[string] = state_dict

            if self.has_initial:
                if (transition['input_state']['is_start'] and transition['input_state'] is not self.curent_state) or (transition['result_state']['is_start'] and transition['result_state'] is not self.curent_state):
                    raise Exception("Start state already defined")
            elif transition['input_state']['is_start'] and not self.has_initial:
                self.has_initial = True
                self.curent_state = transition['input_state']
                self.initial_state = transition['input_state']

            if not self.has_final and transition['result_state']['is_final']:
                self.has_final = True

            state_dict[transition['input_state']] = transition['result_state']

        if not self.has_final:
            raise Exception("Final state is not defined")

    def input(self, string: StringLanguage) -> bool:
        """Input DFA. Mengembalikan true jika accepted, mengembalikan false jika rejected

        Jika rejected, program tidak akan berubah
        """

        if string not in self.transitions or self.curent_state in self.transitions[string]:
            return False

        self.curent_state = self.transitions[string][self.curent_state]

        return True

    def reset(self):
        self.curent_state = self.initial_state

    @property
    def is_final_state(self) -> bool:
        return self.curent_state['is_final']


def all_string_except(exceptions: List[StringLanguage]) -> List[StringLanguage]:
    global language
    result: List[StringLanguage] = []

    for lang in language:

        excluded = False

        for exception in exceptions:
            if lang is exception:
                excluded = True
                break

        if not excluded:
            result.append(lang)

    return result


decl_start = State(is_final=True, is_start=True, name="decl start")
decl_mid_varlet = State(is_final=False, is_start=False, name="decl mid varlet")
decl_mid_const = State(is_final=False, is_start=False, name="decl mid const")
decl_late_const = State(is_final=False, is_start=False, name="decl late const")
decl_final = State(is_final=True, is_start=False, name="decl final")

except_var_let_const = all_string_except([VAR, LET, CONST])

declaration_checker = DFA(
    [
        *[
            Transition(input_state=decl_start, result_state=decl_start, string=strlang) for strlang in except_var_let_const
        ],
        *[
            Transition(input_state=decl_start, result_state=decl_mid_varlet, string=strlang) for strlang in [VAR, LET]
        ],
        Transition(input_state=decl_start,
                   result_state=decl_mid_const, string=CONST),
        Transition(input_state=decl_mid_varlet,
                   result_state=decl_final, string=VARIABLE),
        Transition(input_state=decl_mid_const,
                   result_state=decl_late_const, string=VARIABLE),
        Transition(input_state=decl_late_const,
                   result_state=decl_final, string=ASSIGN),
        *[Transition(input_state=decl_final, result_state=decl_start,
                     string=strlang) for strlang in except_var_let_const],
        *[
            Transition(input_state=decl_final, result_state=decl_mid_varlet, string=strlang) for strlang in [VAR, LET]
        ],
        Transition(input_state=decl_final,
                   result_state=decl_mid_const, string=CONST)
    ]
)

lced_start = State(is_final=True, is_start=True, name="lced start")
lced_mid = State(is_final=False, is_start=False, name="lced mid")
lced_final = State(is_final=True, is_start=False, name="lced final")

assignment = [ASSIGN, PLUSEQ, MINUSEQ, MULTIPLYEQ, DIVIDEEQ, MODULOEQ, POWEQ]
anything_except_assignment = all_string_except(assignment)
anything_except_assignment_and_number = all_string_except(assignment+[NUMBER])

noitaralced_checker = DFA([
    *[Transition(input_state=lced_start, result_state=lced_start,
                 string=strlang) for strlang in anything_except_assignment],
    *[Transition(input_state=lced_start, result_state=lced_mid,
                 string=strlang) for strlang in assignment],
    Transition(input_state=lced_mid, result_state=lced_final, string=VARIABLE),
    * [Transition(input_state=lced_final, result_state=lced_mid,
                  string=strlang) for strlang in assignment],
    *[Transition(input_state=lced_final, result_state=lced_start, string=strlang) for strlang in anything_except_assignment_and_number]
])

arith_start = State(is_final=True, is_start=True, name="arith start")
arith_final_number = State(
    is_final=True, is_start=False, name="arith final number")
arith_op = State(is_final=False, is_start=False, name="arith op")
arith_var = State(is_final=False, is_start=False, name="arith var")

operators = [PLUS, MINUS, MULTIPLY, POW, DIVIDE, MODULO, XOR, BOR, BAND, SHIFT]
anything_except_number_variable = all_string_except([NUMBER, VARIABLE])
anything_except_number_variable_ops = all_string_except(
    [NUMBER, VARIABLE] + operators)

arith_operation_checker = DFA([
    *[Transition(input_state=arith_start, result_state=arith_start, string=strlang)
      for strlang in anything_except_number_variable],
    Transition(input_state=arith_start,
               result_state=arith_final_number, string=NUMBER),
    Transition(input_state=arith_start,
               result_state=arith_var, string=VARIABLE),
    *[Transition(input_state=arith_var, result_state=arith_var,
                 string=strlang) for strlang in assignment],
    *[Transition(input_state=state, result_state=state, string=strlang)
      for state in [arith_var, arith_op, arith_final_number] for strlang in [RBRACKETL, RBRACKETR]],
    *[Transition(input_state=state, result_state=arith_op, string=strlang)
      for state in [arith_final_number, arith_var] for strlang in operators],
    *[Transition(input_state=arith_op, result_state=arith_final_number,
                 string=strlang) for strlang in [NUMBER, VARIABLE]],
    *[Transition(input_state=arith_final_number, result_state=arith_start, string=strlang) for strlang in anything_except_number_variable_ops]
])
