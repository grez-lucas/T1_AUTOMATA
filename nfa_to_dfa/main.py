
from typing import OrderedDict
import sys

def nfaToDfa(file):
    phase = 0
    states = [] 
    transitions = []

    for line in file.readlines():  
        if line in ['Estados\n', 'Alfabeto\n', 'Transiciones\n']:
            phase += 1
        else:
            if phase == 1:
                if line[0] == '>':
                    INITIAL_STATE = line[1:-1].strip()
                    states.append([INITIAL_STATE, 'inicial'])
                elif line[0] == '*':
                    states.append([line[1:-1].strip(), 'final'])
                else:
                    states.append([line[:-1].strip(), 'intermedio'])
            elif phase == 2:
                ALPHABET.append(line[0])
            elif phase == 3:
                A = line.split(" ")
                transitions.append([A[0],A[1],A[3][:-1]])

    truthTable = {}

    for state in states:
        dicc = {}
        for element in ALPHABET:
            array = [ ]
            for transition in transitions:
                if (state[0] == transition[0]) and (element == transition[1]):
                   array.append(transition[2])
            dicc[element] = array
        truthTable[state[0]] = dicc

    toAnalyze = [[INITIAL_STATE]]
    analyzed = []
    analyzedTable = []

    while True:
        if len(toAnalyze) > 0:
            newStates = []
            for states in toAnalyze:
                dicc = {}
                for element in ALPHABET:
                    array = []
                    for state in states:
                        dicc = truthTable[state]
                        for i in dicc[element]:
                            array.append(i)
                    array = list(OrderedDict.fromkeys(array))
                    dicc[element] = array
                    newStates.append(array)        
                analyzedTable.append([states,dicc]) 
                toAnalyze.remove(states)
                analyzed.append(states)
            for state in newStates:
                if state not in analyzed:
                    toAnalyze.append(state) 
        else:  
            break
    
    writeOutput(analyzedTable, ALPHABET, INITIAL_STATE)

def writeOutput(analyzedTable, ALPHABET, INITIAL_STATE):
    outputFile = open("salida.txt", "w")
    outputFile.writelines("Estados" + " \n")
    
    for keys in analyzedTable:
        string = '{' 
        if (keys[0] == [INITIAL_STATE]):
            string = ">" + string 
            string += INITIAL_STATE + ","
        else:
            for element in keys[0]:
                if element == 'C':
                    string = "*" + string
                string += element + ','
        string = string[:-1] + '}'
        outputFile.writelines(string + " \n")

    outputFile.writelines("Alfabeto" + " \n")

    for letra in ALPHABET:
        outputFile.writelines(letra + " \n")

    outputFile.writelines("Transiciones" + " \n")

    for keys in analyzedTable:
        for letra in ALPHABET:
            string = '{'
            for element in keys[0]:
                string += element + ','
            string = string[:-1] + '} ' + letra + " -> {"

            for element in keys[1][letra]:
                string += element + ','
            string = string[:-1] + '}'
            outputFile.writelines(string + " \n")
    outputFile.close()

if (len(sys.argv) == 2):
    inputFile = open(sys.argv[1])
    INITIAL_STATE = None
    ALPHABET = []
    nfaToDfa(inputFile)
    inputFile.close()
else:
    print("Falta un argumento.\nFormato correcto> python main.py 'nombrearchivo'.txt")