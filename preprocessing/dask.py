from functools import reduce
import csv
import dask.dataframe as dd
from preprocessing.preprocess_text import pre_process_text

counter = 0


def factors(n):    
    return sorted(set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))), key = lambda x: x)

def findMiddle(input_list):
    middle = float(len(input_list))/2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return (input_list[int(middle)], input_list[int(middle-1)])[0]


def get_partition_number(n): 
    # n should be length of dataframe
    print('n is ',n)
    if n % 2 != 0:
        n = n - 1 
    facts = factors(n)
    return findMiddle(facts)

def process_partition(partition):
    global counter
    less_toxics = []
    more_toxics = []
    worker = []
    for index, row in partition.iterrows():
        less_toxics.append(pre_process_text(row['less_toxic']))
        more_toxics.append(pre_process_text(row['more_toxic']))
    partition['less_toxic'] = less_toxics
    partition['more_toxic'] = more_toxics
    partition.to_csv('/dask_partitions/partition'+counter+'.csv')
    counter += 1
    return partition