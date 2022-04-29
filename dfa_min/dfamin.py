import os
import re

file_name = "dfa_input"

state = r'[\d\w]+'
symbol = r'[\d\w]'
transition = rf'({state})\s*({symbol})\s*->\s*({state})'

def order_tuple(a,b):
			return (a,b) if a < b else (b,a)

def regex_find_span(text,word):
     pattern = re.compile(word)
     match = pattern.search(text)
     if match:
          return match.span() #returns the index span of a word in a text as list
     else:
          return None

def cleanOutputStr(str):
    clean_str = ''
    for char in str:
        if char != "'":
            clean_str+=char
    return clean_str

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

    
    states = set()

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
            states.add(row[1:-1])
            continue
        elif row[0] == "*":
            original_dfa["e_states"].add(row[1:-1])
            states.add(row[1:-1])
            continue
        else:
            original_dfa["n_states"].add(row[:-1])
            states.add(row[:-1])
        
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


# ==== MINIMIZATION ALGORITHM ====
table = {}

#sort states for table creation
sorted_states = sorted(states)

#Step 1: initialize table with first checkmarks
for i,state in enumerate(sorted_states):
    for state_2 in sorted_states[i + 1:]:
        #XOR,only one can be final
        table[state, state_2] = (state in original_dfa["e_states"]) ^ (state_2 in original_dfa["e_states"])

print(table)
#Step 2: Check unmarked values twice
flag = 1
while flag < 2:
    for key1,key2 in table:
        if table[(key1,key2)] == False:
            for symbol in alphabet:
                state1 = transitions[frozenset({key1,symbol})]
                state2 = transitions[frozenset({key2,symbol})]
                if state1 != state2:
                    if table[order_tuple(max(state1),max(state2))] == True:
                        table[(key1,key2)] = True
                        break
    flag +=1

minimized_states = []
for state1,state2 in table:
    if table[(state1,state2)] == False:
        minimized_states.append({state1} | {state2})

minimized_states2 = []
for i,set1 in enumerate(minimized_states):
    for set2 in minimized_states[i + 1:]:
        if (set1 & set2):
            if (set1 | set2) not in minimized_states2:
                minimized_states2.append( set1 | set2 )
        elif set1 not in minimized_states2:
            minimized_states2.append(set1)

for state in states: # check if any initial states are not included
    if(all([ state not in i for i in minimized_states2])):
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

#write to output
with open (os.path.join(__location__,file_name+"2.txt"), mode='w') as out_file:
    out_file.write("Estados\n")

    out_file.write(">" + cleanOutputStr(str(minimized_dfa["s_state"])) + "\n")
    out_file.write("*" + cleanOutputStr(str(minimized_dfa["e_states"]))+ "\n")
    for value in minimized_dfa["n_states"]:
        out_file.write("{" + cleanOutputStr(str(value)) + "} ")
    out_file.write("\n")
    
        

# prints for testing


print("states", states)

print("alphabet", alphabet)

for key in transitions:
    print(key, transitions[key])

print(transitions[frozenset(['0','B'])])
print(table)
print(minimized_states2)
print("original_dfa",original_dfa)
print("minimized_dfa",minimized_dfa)
print(cleanOutputStr(str(minimized_dfa["s_state"])))

#TODO :remove output2.txt syntax declaration