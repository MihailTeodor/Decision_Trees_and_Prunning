# Decision_Trees_and_Prunning

COME USARE IL CODICE

def main(dataset):
    '''
    elaborate() function generates a decision tree based on file dataset and then pruns it plotting the results (True = light prunning; False = heavy prunning)
    compare() function compares the two implementations of prunning (light and heavy)
    '''
    elaborate(dataset, 5, 50, 3, True)
    compare(dataset, 5, 50, 3)


main("cardata")

Per usare il codice, bisogna passare alla funzione main() il dataset su cui si desidera operare. Il dataset deve avere come prima riga gli attributi e l'attributo target deve essere l'ultimo.

def elaborate(dataset, initial_error_rate, initial_examples_nr, number_of_iterations, m)

def compare(dataset, initial_error_rate, initial_examples_nr, number_of_iterations)

I parametri delle due funzioni rappresentano: 
		• file - denota il dataset su cui operare; 
		• initial_error_rate - denota la percentuale dell'errore da introdurre nel grow set (la percentuale aumenta dello 25% ad ogni iterazione del ciclo principale delle rispettive funzioni); 
		• initial_examples_nr - denota il numero iniziale di esempi presi casualmente dall'intero dataset sul quale costruire i tre dataset(grow set, validation set e test set) usati dall'elaborazione. 
		  Il numero di esempi viene aumentato ad ogni iterazione interna di un numero pressato; • number_of_iterations - denota il numero delle iterazioni su cui fare la media ( i grafici mostrati qui sono ottenuti come media su 10 iterazioni); 
		• light - se True verrà usata l'implementazione 'light' della procedura di potatura; se False verrà usata quella 'heavy';


RIFERIMENTI

Questo progetto è stato svolto su base di quanto esposto in R&N 2009 §18.3,  Mitchell 1997, cap. 3. Inoltre è stato consultato il progetto al seguente link: https://github.com/yichen611/DecisionTreeWithPruning.

