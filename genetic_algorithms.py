from math import ceil, log2
from random import randint

import numpy
from numpy import random
file = open("result.txt", 'w')
fin = open("date.txt", 'r')

dimension = int(fin.readline())
p = int(fin.readline())
bounds = [int(nr) for nr in fin.readline().split(" ")]
parameters = [int(nr) for nr in fin.readline().split(" ")]
crossover_probability = float(fin.readline())
mutation_probability = float(fin.readline())
nr_generations = int(fin.readline())


length = ceil(log2((bounds[1]-bounds[0]) * 10 ** p)) #calculam lungimea fixa a unui cromozom

population = [[0 for _ in range(length)] for y in range(dimension)]
x = [0 for _ in range(dimension)]
f = [0 for _ in range(dimension)]
intervals = [0 for _ in range(dimension+1)]
selected_chromosomes = []
def generate_chromosome():
    for i in range(dimension):
        for j in range(length):
            population[i][j] = randint(0, 1) #generam random populatia initiala

def generate_value(): #transformam valoarea codificata
    for i in range(dimension):
        y = (bounds[1] - bounds[0]) / (2 ** length - 1)
        x[i] = 0
        for j in range(length-1, 0, -1):
            if(population[i][j]):
                x[i] += y
            y *= 2
        x[i] += bounds[0]
        x[i]= round(x[i], p)

def apply_function(): #functia de fitness
    for i in range(dimension):
        f[i] = parameters[0] * (x[i] ** 2) + parameters[1] * x[i] + parameters[2]

def calc_intervals(sum_f): #generam intervalele de probabilitate
    for i in range(1, dimension):
        intervals[i] = intervals[i-1] + f[i-1]/sum_f
    intervals[dimension] = float(1)

generate_chromosome()
generate_value()
apply_function()
sum_f = sum(f)
calc_intervals(sum_f)

def binary_search(x): #cautare binara pt a afla prima valoare mai mare decat un x dat
    low = 0
    high = dimension - 1

    while low <= high:
        mid = (high + low) // 2
        if intervals[mid] < x:
            low = mid + 1
        elif intervals[mid] > x:
            high = mid - 1
    return low

def select_chromosome(population, x, f, j):
    for i in range(dimension):
        u = random.uniform()
        selected_chromosomes.append(binary_search(u))
        if j == 0:
            file.write('\nu=' + str(u) + ' selectam cromozomul ' + str(selected_chromosomes[i]))
    population1 = [[ 0 for _ in range(length)] for y in range(dimension)]
    x1 = [0 for _ in range(dimension)]
    f1 = [0 for _ in range(dimension)]
    for i in range(dimension):
        population1[i] = population[selected_chromosomes[i]-1]
        x1[i] = x[selected_chromosomes[i]-1]
        f1[i] = f[selected_chromosomes[i]-1]

    population = population1
    x = x1
    f = f1
    if j == 0:
        file.write('\nDupa selectie:\n')
        for i in range(dimension):
            file.write(str(i + 1) + ": " + ''.join(map(str, population[i])) + ' x= ' + str(x[i]) + ' f=' + str(f[i]) + '\n')

    participants = []
    if j == 0:
        file.write('\nProbabilitatea de incrucisare ' + str(crossover_probability))
    for i in range(dimension):
        u = random.uniform()
        if u < crossover_probability :
            if j == 0:
                file.write('\n' + str(i+1) + ': ' + ''.join(map(str, population[i])) + ' u= ' + str(u) + ' < ' + str(crossover_probability) + ' participa')
            participants.append(i)
        elif j == 0:
            file.write('\n' + str(i + 1) + ': ' + ''.join(map(str, population[i])) + ' u= ' + str(u))

    while len(participants) > 1:
        cr1 = random.choice(participants)
        participants.remove(cr1)
        cr2 = random.choice(participants)
        participants.remove(cr2)
        pct = random.randint(0,length)
        if j == 0:
            file.write('\n Recombinare dintre cromozomul ' + str(cr1+1) + ' cu cromozomul '+ str(cr2+1) + ':\n')
            file.write(''.join(map(str, population[cr1])) + ' ' + ''.join(map(str, population[cr2])) + ' punct ' + str(pct)+ '\n')
        for i in range(pct):
            population[cr1][i], population[cr2][i] = population[cr2][i], population[cr1][i]
        if j == 0:
            file.write('Rezultat   ' + ''.join(map(str, population[cr1])) + ' ' + ''.join(map(str, population[cr2])))
    return population



def generate_mutations(j):
    k = 0
    for i in range(dimension):
        u = random.uniform() #genereaza o variabila uniforma u
        if u < mutation_probability:
            if j == 0:
                if k == 0:
                    file.write('\nProbabilitate de mutatie pentru fiecare gena ' + str(mutation_probability))
                    file.write('\nAu fost modificati cromozomii:\n' + str(i+1))
                    k += 1
                else:
                    file.write('\n' + str(i+1))
            p = random.randint(0, length) #genereaza o pozitie aleatoare
            population[i][p] = (population[i][p] + 1) % 2 #trece gena la complement
    if j == 0:
        file.write('\n')
    return k



file.write("Populatia initiala\n")
for i in range(dimension):
    file.write( str(i+1) + ": " + ''.join(map(str, population[i])) + ' x= ' + str(x[i]) + ' f=' + str(f[i]) + '\n')

file.write('\nProbabilitati selectie\n')
for i in range(dimension):
    file.write('cromozom   ' + str(i+1) + ' probabilitate ' + str(f[i]/sum_f) + '\n')

file.write('\nIntervale probabilitati selectie\n')
for i in range(dimension+1):
    file.write(str(intervals[i])+' ')

population = select_chromosome(population, x, f, 0)

file.write('\n\nDupa recombinare:\n')
generate_value() #decodific noii cromozomi
apply_function()
for i in range(dimension):
    file.write(str(i + 1) + ": " + ''.join(map(str, population[i])) + ' x= ' + str(x[i]) + ' f=' + str(f[i]) + '\n')

if(generate_mutations(0)): #daca s-au produs mutatii decodific din nou si calculez f(x)
    generate_value()
    apply_function()
    file.write('\nDupa mutatie:\n')
    for i in range(dimension):
        file.write(str(i + 1) + ": " + ''.join(map(str, population[i])) + ' x= ' + str(x[i]) + ' f=' + str(f[i]) + '\n')

max_f = max(f)
ind = numpy.argmax(f)
file.write('\nElementul elitist este:\n')
file.write(str(ind + 1) + ": " + ''.join(map(str, population[ind])) + ' x= ' + str(x[ind]) + ' f=' + str(f[ind]) + '\n')

file.write('\nEvolutia maximului')
for i in range(1, nr_generations):
    sum_f = sum(f)
    calc_intervals(sum_f)
    population = select_chromosome(population, x, f, i)
    generate_value()
    apply_function()
    generate_mutations(i)
    generate_value()
    apply_function()
    if max_f < max(f):
        max_f = max(f) #retin in max_f cea mai buna valoare
    file.write('\n' + str(max(f)))

