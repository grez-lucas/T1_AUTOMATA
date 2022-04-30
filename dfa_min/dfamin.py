import os
import re

file_name = input("Please enter the file name of the dfa you wish to minimize:\n")

state = r'[\d\w]+'
symbol = r'[\d\w]'
transition = rf'({state})\s*({symbol})\s*->\s*({state})'


def order_tuple(a, b):
    return (a, b) if a < b else (b, a)


def regex_find_span(text, word):
    pattern = re.compile(word)
    match = pattern.search(text)
    if match:
        return match.span()  # returns the index span of a word in a text as list
    else:
        return None


def cleanOutputStr(str):
    clean_str = ''
    if str[:10] == 'frozenset(':
        str = str[10:-1]
    for char in str:
        if char != "'":
            clean_str += char
    return clean_str

def findSetListIndex(set_list, value):
    value = str(value)[2:-2]
    for set in set_list:
        if value in set:
            return set_list.index(set)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


with open(os.path.join(__location__, file_name+".txt")) as file:
    fileIsValid = True

    contents = file.read()
    state_span = regex_find_span(contents, r'\bEstados\n')
    alphabet_span = regex_find_span(contents, r'\bAlfabeto\n')
    transition_span = regex_find_span(contents, r'\bTransiciones\n')

    original_dfa = {"s_state": set(), "n_states": set(), "e_states": set()}
    minimized_dfa = {"s_state": set(), "n_states": set(), "e_states": set()}

    states = set()

    alphabet = set()

    transitions = {}

    file.seek(state_span[1]+1)  # begin reading from Estados\n onwards
    

    for row in file:

        if row == "Alfabeto\n":
            break
        if row == r'^\s+\n$':  # if row is empty, continue to the next iteration
            continue

        if row[0] == ">":
            original_dfa["s_state"].add(row[1:-1])
            states.add(row[1:-1])
            continue
        elif row[0] == "*":
            original_dfa["e_states"].add(row[1:-1])
            states.add(row[1:-1])
            continue
        else:
            original_dfa["n_states"].add(row[:-1])
            states.add(row[:-1])

        

    file.seek(alphabet_span[1]+8)  # begin reading from Alfabeto\n onwards
    

    for row in file:
        if row == "Transiciones\n":
            break
        if row == r'^\s+\n$':  # if row is empty, continue to the next iteration
            continue

        alphabet.add(row[:-1])

        

    file.seek(transition_span[1])  # begin reading from Alfabeto\n onwards
    

    for row in file:
        if row == r'^\s+\n$':  # if row is empty, continue to the next iteration
            continue

        pattern = re.compile(transition)
        match = pattern.search(row)

        if match:
            transitions[frozenset([match.group(1), match.group(2)])] = set(
                match.group(3))

        


# ==== MINIMIZATION ALGORITHM ====
table = {}

# sort states for table creation
sorted_states = sorted(states)

# Step 1: initialize table with first checkmarks
for i, state in enumerate(sorted_states):
    for state_2 in sorted_states[i + 1:]:
        # XOR,only one can be final
        table[state, state_2] = (state in original_dfa["e_states"]) ^ (
            state_2 in original_dfa["e_states"])

# Step 2: Check unmarked values twice
flag = 1
while flag < 2:
    for key1, key2 in table:
        if table[(key1, key2)] == False:
            for symbol in alphabet:
                state1 = transitions[frozenset({key1, symbol})]
                state2 = transitions[frozenset({key2, symbol})]
                if state1 != state2:
                    if table[order_tuple(max(state1), max(state2))] == True:
                        table[(key1, key2)] = True
                        break
    flag += 1

minimized_states = []
for state1, state2 in table:
    if table[(state1, state2)] == False:
        minimized_states.append({state1} | {state2})

minimized_states2 = []
for i, set1 in enumerate(minimized_states):
    for set2 in minimized_states[i + 1:]:
        if (set1 & set2):
            if (set1 | set2) not in minimized_states2:
                minimized_states2.append(set1 | set2)
        elif set1 not in minimized_states2:
            minimized_states2.append(set1)

for state in states:  # check if any initial states are not included
    if(all([state not in i for i in minimized_states2])):
        minimized_states2.append({state})
# write final and initial state values to minimized_dfa
max_finals = 0
for state in minimized_states2:
    if original_dfa["s_state"] & state:
        minimized_dfa["s_state"] = state
    elif original_dfa["e_states"] & state:
        final_count = len(original_dfa["e_states"] & state)
        if final_count > max_finals:
            max_finals = final_count
            minimized_dfa["e_states"] = state
    else:
        minimized_dfa["n_states"].add(str(state)[2:-2])
# write minimized transitions
minimized_transitions = {}
for set in minimized_states2:
    for (state1, symbol) in transitions:
        # if the set contains the state and the destination is not part of the set...
        if ( set & {state1, symbol} ) and ( transitions[frozenset({state1, symbol})] not in set ) : 
            # new_destination will be minimized set containing previous destination set
            new_destination = minimized_states2[findSetListIndex(minimized_states2, transitions[frozenset({state1, symbol})])]
            if state1 in alphabet: #because sets are not always ordered
                symbol = state1
            minimized_transitions[frozenset({frozenset(set), symbol})] = new_destination
            continue

# write to output
with open(os.path.join(__location__, "dfa_output.txt"), mode='w') as out_file:
    out_file.write("Estados\n")

    out_file.write(">" + cleanOutputStr(str(minimized_dfa["s_state"])) + "\n")
    out_file.write("*" + cleanOutputStr(str(minimized_dfa["e_states"])) + "\n")
    for value in minimized_dfa["n_states"]:
        out_file.write("{" + cleanOutputStr(str(value)) + "} ")
    out_file.write("\n")
    out_file.write("Alfabeto\n")
    for value in alphabet:
        out_file.write(str(value) + "\n")
    out_file.write("Transiciones\n")
    for key1,key2 in minimized_transitions:
        if key1 in alphabet:
            
            out_file.write(cleanOutputStr(str(key2)) + " " + str(key1))
        else:
            out_file.write(cleanOutputStr(str(key1)) + " " + str(key2))
        out_file.write(" -> " + cleanOutputStr(str(minimized_transitions[frozenset({key1,key2})])) + "\n")