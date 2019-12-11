import argparse
import math
import numpy as np
from itertools import combinations

#Author: Adam Davis
#Date: 04/09/2019
#Class: CSE 5243
#title: Programming Assingment 2
#Discription: This program takes in a database of transations then prints the subsets of transactions
#the occur in the frequency that the user provides
#command Line example: python apriori.py -database_file database.txt -minsupp .5 -output_file output.txt

parser = argparse.ArgumentParser() #create command line Parser

#add Command line arguments
parser.add_argument('-database_file')   
parser.add_argument('-minsupp')
parser.add_argument('-output_file')

args = parser.parse_args() # Send all arguments to args

database_file = str(args.database_file)   #database.txt
minSup = float(args.minsupp) #Minimum support
output_file = str(args.output_file) #output.txt

def generate_F1(database):
	F1 = []  #initialize F1
	minCount = int(database[0][0]*minSup) #The count to hit min support

	candidates = database[0][1] #num of starting canadidates
	for x in range(candidates): #initilize all candidates with a count of 0
		F1.append([x,0])
	for x in range(1, database[0][0] + 1): #Count the num of occurences of each canidate
		for y in range(len(database[x])):
			F1[database[x][y]][1] += 1
	for x in range(candidates -1,  -1, -1): #remove all that don't make the count 
		if(F1[x][1] < minCount):
			del F1[x]
	return[ x[0] for x in F1] #return F1

def generate_candidate(LastFreq_set, k):
	if(k != 1): #check it is F-1
		uniq_elem = []   #intialize uniq_elem
		for x in range(len(LastFreq_set)): #get all unique elements
			for y in range(k):
				if(LastFreq_set[x][y] not in uniq_elem):
					uniq_elem.append(LastFreq_set[x][y])
	else:
		uniq_elem = LastFreq_set  #if F-1 unique elements = lastFreq_set

	return(map(list, combinations(uniq_elem, k+1)))
	
def prune_candidate(LastFreq_set, candidates, k): #if a subset of a transaction is not in F-K-1 then remove from candidates
	for x in range(len(candidates) -1, -1, -1):
		attempts = (map(list, combinations(candidates[x], k))) 
		for n in range(k+1):
			if attempts[n] not in LastFreq_set:
				del candidates[x]
				break
	return candidates
	
def count_support(candidates, database):  #create a list of the count that a candidates appears in the database transactions
	count = []
	for x in range(len(candidates)):
		holdCount = 0
		for y in range(len(database)):
			if(set(candidates[x]).issubset(set(database[y]))):
				holdCount += 1
		count.append(holdCount)
	return count
	
	
def eliminate_candidate(support, candidates, minCount): 

	for x in range(len(candidates) -1,  -1, -1): #if candidate does not fit support then it is elemenated
		if(support[x] < minCount):
			del candidates[x]
	return candidates
	
def output_freq_itemsets(freq_set):

	f = open(output_file, "w") #open output file   
	 
	items = len(freq_set[0]) #get number of items in output
	
	transactions = 0          #intiate number of transactions
	for n in range(len(freq_set)): #count all transactions
		transactions += len(freq_set[n])
		
	f.write(`transactions` + " " + `items`+ "\n") #print items and transactions at top of output
	
	for x in range(len(freq_set) -1): #rotate through each F set
		for p in range(len(freq_set[x]) ): #rotate through each transaction in F set
			if(x > 0):    #if there is more than one value in the transaction (to remove [] and commas
				for n in range(len(freq_set[x][p])):  #rotate through each transtion item
					f.write(`freq_set[x][p][n]` + " ")
				f.write("\n")
			else:
 				f.write(`freq_set[x][p]` + "\n") 
	f.close()   #close output file
	

def apriori(database):

	k = 1       #intitiate F-K value
	freq_set = []   #initiate freq_set of transactions
	count = []
	freq_set.append(generate_F1(database))  #generate the F-1

	while len(freq_set[k -1]) > 0:  #while there is still values in the previous F-k
		candidates = []
		candidates = generate_candidate(freq_set[k-1], k) #generate all possible candidates
		if(k != 1):
			candidates = prune_candidate(freq_set[k-1], candidates, k) #prune the possible candidates
		
		support = count_support(candidates, database)  #get support of each candidate
		eliminate_candidate(support, candidates, database[0][0]*minSup) #Remove all candidates that don't meet the support
		
		freq_set.append( eliminate_candidate(support, candidates, int(database[0][0]*minSup))) #add to list of transactions
	
		k += 1 #increment k
		
	output_freq_itemsets(freq_set) #print all transaction that meet the requirments of the support



def read_database():#convert the database file to a two dimensional list


	fp = open(database_file, 'r') #open database.txt
	
	database = [] #initialize empty list
	database.append( map(int, fp.readline().split())) #get first line

	
	for x in range(database[0][0]): #fill in list with each transaction
		database.append(map(int, fp.readline().split()))
	
	fp.close() #close database.txt
	
	return database


def main():
	database = read_database() #create a list repersentation of the database
	apriori(database) #start apriori methods


main()
