class State:
    def __init__(self, name) -> None:
        self.name = name
        self.start = False
        self.final = False
        self.transition_rules = dict()

    #maps a state to a given symbol
    def add_rule(self, reading_symbol, destination_state):
        self.transition_rules[reading_symbol] = destination_state

    def read_symbol(self, reading_symbol):
        return self.transition_rules[reading_symbol]

    def set_final(self, isFinal):
        self.final = isFinal

    def set_start(self, isStart):
        self.start = isStart

    def get_name(self):
        return self.name

    def is_final(self):
        return self.final

    def __str__(self) -> str:
        return ', '.join(['Name: ' + self.name, 
            'Start: ' + str(self.start), 
            'Final: ' + str(self.final),
            'Transition Rules: ' + ', '.join([r + ':' + self.transition_rules[r].get_name() for r in self.transition_rules])])


class DFA:
    def __init__(self) -> None:
        self.states = {}
        self.alphabet = set()
        self.start = None

    #creates a new dfa as specified by input dfa file.
    def new(self, dfa_file_name='dfa.txt'):
        self.states = {}
        self.alphabet = set()
        self.start = None
        with open(dfa_file_name) as dfa_file:
            #read states
            state_name_list = dfa_file.readline().rstrip().split(',')
            for state_name in state_name_list: self.states[state_name] = State(state_name)

            #read alphabet
            letters = dfa_file.readline().rstrip().split(',')
            for l in letters: self.alphabet.add(l)

            #set start state
            start_state = dfa_file.readline().rstrip()
            self.states[start_state].set_start(True)
            self.start = self.states[start_state]

            #set final state(s)
            final_states = dfa_file.readline().rstrip().split(',')
            for final_state in final_states: self.states[final_state].set_final(True)

            #set transition rules (number of rules = #of states * size of alphabet)
            for _ in range(len(self.states) * len(self.alphabet)):
                rule = dfa_file.readline().rstrip().split(',')
                self.states[rule[0]].add_rule(rule[1], self.states[rule[2]])

    #simulates dfa for every string in input file and writes results to output file.
    def run(self, input_file_name='input.txt', output_file_name='output.txt'):
        #clear output file
        with open(output_file_name, 'r+') as out:
                    out.truncate(0)
                    out.close()
        #read input file, follow transition rules for each string in file and write result to output.
        with open(input_file_name) as input_file:
            with open(output_file_name, 'a') as out:
                for s in input_file:
                    input_string = s.rstrip().split(',')
                    current = self.start
                    for letter in input_string:
                        current = current.read_symbol(letter)
                    if current.is_final():
                        out.write('accept\n')
                    else:
                        out.write('reject\n')
                    current = self.start
                out.close()
                    
    def __str__(self) -> str:
        return 'States:\n' + '\n'.join(['  ' + '\n  '.join([str(self.states[s]) for s in self.states]), 
            'Alphabet: {' + ', '.join([s for s in self.alphabet]) + '}'])


def main():
    test_DFA = DFA()
    test_DFA.new()
    #print(test_DFA)
    test_DFA.run()
    #test_DFA.new('test_dfa_1.txt')
    #print(test_DFA)
    #test_DFA.run('test_input_1.txt')
    #test_DFA.new('test_dfa_2.txt')
    #print(test_DFA)
    #test_DFA.run('test_input_2.txt')
    #test_DFA.new('test_dfa_3.txt')
    #print(test_DFA)
    #test_DFA.run('test_input_3.txt')


if __name__ == '__main__':
    main()
