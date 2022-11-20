from .string import StringLanguage
from typing import List, Dict, TypedDict


class State(TypedDict):
    is_start: bool
    is_final: bool


class Transition(TypedDict):
    input_state: State
    result_state: State
    string: StringLanguage


class DFA:
    transitions: Dict[StringLanguage, Dict[State, State]]
    curent_state: State
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

    @property
    def is_final_state(self) -> bool:
        return self.curent_state['is_final']


start_state = State(is_start=True, is_final=False)
final_state = State(is_start=False, is_final=True)


dfa_variable = DFA(
    [
        # Transition(input_state=)
    ]
)

dfa_operation = DFA(
    []
)
