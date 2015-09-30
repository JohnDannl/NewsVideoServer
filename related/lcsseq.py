#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Longest common subsequence using dynamic programming algorithm

Created on 2014-10-18

@author: JohnDannl
'''
def getLCS(X, Y):
    #Computing the length of the LCS
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[m][n]

def LCS(X, Y):
    #Computing the length of the LCS
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def backTrack(C, X, Y, i, j):
    # Reading out an LCS
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    if i == 0 or j == 0:
        return ""
    elif X[i-1] == Y[j-1]:
        return backTrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)
        
def backTrackAll(C, X, Y, i, j):
    # Reading out all LCSs
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    if i == 0 or j == 0:
        return set([""])
    elif X[i-1] == Y[j-1]:
        return set([Z + X[i-1] for Z in backTrackAll(C, X, Y, i-1, j-1)])
    else:
        R = set()
        if C[i][j-1] >= C[i-1][j]:
            R.update(backTrackAll(C, X, Y, i, j-1))
        if C[i-1][j] >= C[i][j-1]:
            R.update(backTrackAll(C, X, Y, i-1, j))
        return R
    
def printDiff(C, X, Y, i, j):
    # Print the diff
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    if i > 0 and j > 0 and X[i-1] == Y[j-1]:
        printDiff(C, X, Y, i-1, j-1)
        print "  " + X[i-1]
    else:
        if j > 0 and (i == 0 or C[i][j-1] >= C[i-1][j]):
            printDiff(C, X, Y, i, j-1)
            print "+ " + Y[j-1]
        elif i > 0 and (j == 0 or C[i][j-1] < C[i-1][j]):
            printDiff(C, X, Y, i-1, j)
            print "- " + X[i-1]
            
def getSentenceSim(sent1,sent2):
    # First,convert to utf-8 code
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    length= len(sent1) if len(sent1)>len(sent2) else len(sent2)
#     print 'len:',getLCS(sent1,sent2)
    if length==0:
        return 1.0
    return getLCS(sent1,sent2)/float(length)
                
if __name__=='__main__':
#     X = "AATCC"
#     Y = "ACACG"
    X='下面是中文bug'
    Y='这是的一个bug'
    X=X.decode('utf-8')
    Y=Y.decode('utf-8')
    m = len(X)
    print m
    n = len(Y)
    C = LCS(X, Y)
    print "Longest subsequence: %s" % getLCS(X,Y)
    print "Some LCS: '%s'" % backTrack(C, X, Y, m, n)
    print "All LCSs: %s" % backTrackAll(C, X, Y, m, n)
    print getSentenceSim(X,Y),getSentenceSim(X,X)