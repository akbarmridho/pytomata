from .string import StringLanguage
from typing import List, Dict, TypedDict


class State(TypedDict):
    name: str
    is_final: bool


class Transition(TypedDict):
    input_state: State
    result_state: State
    string: StringLanguage


class DFA:
    transitions: Dict[StringLanguage, Dict[State, State]]
    curent_state: State

    def __init__(self, transitions: List[Transition]):
        self.transitions = {}

        for transition in transitions:
            string = transition['string']
            state: Dict[State, State]

            if string in self.transitions:
                state = self.transitions[string]
            else:
                state = {}
                self.transitions[string] = state

            state[transition['input_state']] = transition['result_state']

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
