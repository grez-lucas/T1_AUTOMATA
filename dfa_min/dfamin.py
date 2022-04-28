import os
import re

file_name = "dfa_input"

state = r'[\d\w]+'
symbol = r'[\d\w]'
transition = rf'({state})\s*({symbol})\s*->\s*({state})'

def regex_find_span(text,word):
     pattern = re.compile(word)
     match = pattern.search(text)
     if match:
          return match.span() #returns the index span of a word in a text as list
     else:
          return None

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))




with open(os.path.join(__location__, file_name+".txt")) as file:
    fileIsValid = True

    contents = file.read()
    state_span = regex_find_span(contents,r'\bEstados\n')
    alphabet_span = regex_find_span(contents,r'\bAlfabeto\n')
    transition_span = regex_find_span(contents,r'\bTransiciones\n')

    original_dfa = { "s_state" : set() , "n_states" : set() , "e_states" : set()}
    minimized_dfa = { "s_state" : set() , "n_states" : set() , "e_states" : set()}

    alphabet = set()

    transitions = {}


    print(contents + '\n')
    print(state_span)


    file.seek(state_span[1]+1)          #begin reading from Estados\n onwards
    row_counter, valid_row_counter = 0 , 0

    for row in file:
                    
        if row == "Alfabeto\n":
            break
        if row == r'^\s+\n$':       #if row is empty, continue to the next iteration
            continue
    
        if row[0] == ">":
            original_dfa["s_state"].add(row[1:-1])
            continue
        elif row[0] == "*":
            original_dfa["e_states"].add(row[1:-1])
            continue
        else:
            original_dfa["n_states"].add(row[:-1])
        
        row_counter+=1
    
    file.seek(alphabet_span[1]+8)          #begin reading from Alfabeto\n onwards
    row_counter, valid_row_counter = 0 , 0

    for row in file:
        if row == "Transiciones\n":
            break
        if row == r'^\s+\n$':       #if row is empty, continue to the next iteration
            continue
        
        alphabet.add(row[:-1])

        row_counter+=1
    

    file.seek(transition_span[1])          #begin reading from Alfabeto\n onwards
    row_counter, valid_row_counter = 0 , 0

    for row in file:
        if row == r'^\s+\n$':       #if row is empty, continue to the next iteration
            continue
        
        pattern = re.compile(transition)
        match = pattern.search(row)
        
        if match:
            transitions[frozenset([match.group(1),match.group(2)])] = set(match.group(3))

        row_counter+=1


    # minimization algorithm
    


    # print for testing
    for key in original_dfa:
        print(key, original_dfa[key])

    print(alphabet)

    for key in transitions:
        print(key, transitions[key])

    print(transitions[frozenset(['0','B'])])
