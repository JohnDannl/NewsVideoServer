#!/urs/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-10-18

@author: JohnDannl
'''
def longest_common_substring(s1, s2):
    # return the longest common substring,note: is different from subsequence
    s1=s1.decode('utf-8')
    s2=s2.decode('utf-8')
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def get_longest_common_substring(s1, s2):
    # return the longest common substring,note: is different from subsequence
    s1=s1.decode('utf-8')
    s2=s2.decode('utf-8')
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return longest

def getSentenceSim(sent1,sent2):
    sent1=sent1.decode('utf-8')
    sent2=sent2.decode('utf-8')
    length= len(sent1) if len(sent1)>len(sent2) else len(sent2)
    if length==0:
        return 1.0
    return get_longest_common_substring(sent1, sent2)/float(length)

if __name__=='__main__':
    X = "AATCC"
    Y = "ACACG"
    print "Longest substring length: %s" % get_longest_common_substring(X,Y)
    print "Some LCS: '%s'" % longest_common_substring(X,Y)
    X='下面是中文bug'
    Y='这是的一个bug'
    print getSentenceSim(X,Y)