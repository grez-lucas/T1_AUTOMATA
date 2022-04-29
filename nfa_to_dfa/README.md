# NFA to DFA

## *Entrada:*
El archivo principal del algoritmo es *'main.py'*. Al momento de ejecutar el programa, se debe escribir un un tercer argumento. Este debe contener el nombre del archivo de entrada con el NFA (añadiendo el *'.txt'*). 

Ejemplo:

          console> python main.py "archivoentrada".txt

*Notar que este archivo tiene una estructura fija, con la cual representaremos autómatas. Una sección con los estados, una sección con el alfabeto y otra con las transiciones. El estado inicial es aquel precedido por un símbolo ">", mientras que los estados finales son aquellos precedidos por un "***". Por otro lado las transiciones tienen el siguiente formato: qi simbolo -> qf , en donde qi es el estado en donde comienza la transición, símbolo es un elemento del alfabeto, y qf es el estado a dónde se llega por medio de la transición.*

## *Salida:*

 La aplicación crea un archivo llamado *'salida.txt'*, el que tiene la misma estructura que el archivo de entrada, salvo en este el caso que los estados sean subconjuntos. 
