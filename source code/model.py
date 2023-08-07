# Dy, Sealtiel
# Ong, Camron
# Tan, Arvin

class PDA:
    def __init__(self):
        self.alphabet = []
        self.states = []
        self.stack = ['Z']
        self.inputs = []
        self.stack_symbol = None
        self.start_state = None
        self.current_state = None
        self.possible = True
        self.idx = 0
        self.step = 0
        self.is_first_step = True

    def move_next_transition(self,input_symbol):
        next_trans = self.current_state.next_transition(input_symbol,self.stack[-1])
        if(next_trans):
            if(next_trans.pop_char != ""):
                self.stack.pop()
            if(next_trans.push_char != ""):
                self.stack.append(next_trans.push_char)
            self.current_state = next_trans.to_state
            if(next_trans.input_symbol == ""):
                return 1
            return 2
        else:
            return 0

    def string_accepted(self):
        return self.current_state.is_final and not self.stack and self.possible

class State:
    def __init__(self, state_id, name):
        self.state_id = state_id
        self.is_final = False
        self.transitions = []
        self.name = name

    def next_transition(self, input_symbol, pop_char):
        for i in range(len(self.transitions)):
            trans = self.transitions[i]
            if (trans.pop_char == "" or trans.pop_char == pop_char) and trans.input_symbol == input_symbol:
                return trans

        input_symbol = ""
        for i in range(len(self.transitions)):
            trans = self.transitions[i]
            if (trans.pop_char == "" or trans.pop_char == pop_char) and trans.input_symbol == input_symbol:
                return trans
        return None

class Transition:
    def __init__(self, from_state, to_state, input_symbol, pop_char, push_char):
        self.from_state = from_state
        self.to_state = to_state
        self.input_symbol = input_symbol
        self.pop_char = pop_char
        self.push_char = push_char
