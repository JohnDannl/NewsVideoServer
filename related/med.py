#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Minimum edit distance using dynamic programming algorithm

Created on 2014-10-18

@author: JohnDannl
'''

def levenshtein(s1, s2):
    # Dynamic Programming algorithm, with the added optimization that only the last two rows 
    # of the dynamic programming matrix are needed for the computation
    s1=s1.decode('utf-8')
    s2=s2.decode('utf-8')
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

# Another version using a mathmatic package NumPy is 40% faster

# def levenshtein(source, target):
#     source=source.decode('utf-8')
#     target=target.decode('utf-8')
#     if len(source) < len(target):
#         return levenshtein(target, source)
#  
#     # So now we have len(source) >= len(target).
#     if len(target) == 0:
#         return len(source)
#  
#     # We call tuple() to force strings to be used as sequences
#     # ('c', 'a', 't', 's') - numpy uses them as values by default.
#     source = np.array(tuple(source))
#     target = np.array(tuple(target))
#  
#     # We use a dynamic programming algorithm, but with the
#     # added optimization that we only need the last two rows
#     # of the matrix.
#     previous_row = np.arange(target.size + 1)
#     for s in source:
#         # Insertion (target grows longer than source):
#         current_row = previous_row + 1
#  
#         # Substitution or matching:
#         # Target and source items are aligned, and either
#         # are different (cost of 1), or are the same (cost of 0).
#         current_row[1:] = np.minimum(
#                 current_row[1:],
#                 np.add(previous_row[:-1], target != s))
#  
#         # Deletion (target grows shorter than source):
#         current_row[1:] = np.minimum(
#                 current_row[1:],
#                 current_row[0:-1] + 1)
#  
#         previous_row = current_row
#  
#     return previous_row[-1]

def getSentenceSim(sent1,sent2):
    # First,convert to utf-8 code
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    length= len(sent1) if len(sent1)>len(sent2) else len(sent2)
#     print 'len:',getLCS(sent1,sent2)
    if length==0:
        return 1.0
    return 1.0-levenshtein(sent1, sent2)/float(length)
if __name__=='__main__':
    X = "AATCC"
    Y = "ACACG"
    print levenshtein(X, Y)