#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit
import copy

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        word=word.lower()
        pronounciationDictionaryTotal=nltk.corpus.cmudict.dict()
        if word in pronounciationDictionaryTotal.keys():
            lst=pronounciationDictionaryTotal[word]
            #print '\npronounciation', word, lst
            syllable = []
            #syllable.clear()
            for proInst in lst:
                i=0
                for ch in proInst:
                    #print '\nInside For'


                    if(any(j.isdigit() for j in ch)):

                    #if ch[-1].isdigit():
                        i = i + 1
                syllable.append(i)
            #print '\n Syllable count',syllable
            return min(syllable)

        else:
            return 1



        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!

        return 1

    def rhymes(self, a, b):
        firstVowelFound=False
        firstConsonantFound=False
        #a="tree"
        #b="debris"
        word1=copy.copy(a)
        word2=copy.copy(b)
        word1=word1.lower()
        word2=word2.lower()
        #print("word1++",word1)
        #print("word2++",word2)
        vowelsLst=['AO','AA','IY','UW','EH','IH','UH','AX','AH','AE','EY','AY','OW','AW','OY','ER','AXR','EH R','UH R','AO R','AA R','AA R','IH R','IY R','AW R']
        consonantsLst=['P','B','T','D','K','G''CH','JH','F','V','TH','DH','S','Z','SH','ZH','HH','M','EM','N','EN','NG','ENG','L','EL','R','DX','NX','Y','W','Q']
        pronounciationDictionaryTotal = nltk.corpus.cmudict.dict()
        if word1 in pronounciationDictionaryTotal.keys():
            proWord1 = pronounciationDictionaryTotal[word1]
        else:
            return False
        #print("proWord1++",proWord1)
        if word2 in pronounciationDictionaryTotal.keys():
            proWord2 = pronounciationDictionaryTotal[word2]
        else:
            return False
        #print("proWord2++",proWord2)
        #
        normWord1=[]
        normWord2=[]
        lenNormWord1=[]
        lenNormWord2=[]
        normWord1Dict=dict()
        normWord2Dict=dict()
        for proInst in proWord1:
            firstVowelFound=False
            #firstConsonantFound=False

            str=[]
            pron=proInst
            #print("pron-->", pron)
            i=0
            for ch in pron:
                temp=ch
                lenTemp=len(temp)
                x=''

                #chLen=len(ch)
                #print("ch-->",ch)
                if lenTemp==3 and ch[-1].isdigit():
                    x=ch[:lenTemp-1]
                    #print("Inside IF-->",x)
                elif lenTemp==4 and ch[-2].isdigit():
                    x=ch[:2]+" "+ch[3]
                    #print("Inside ELIF-->",x)
                else:
                    x=ch

                if x in vowelsLst and firstVowelFound==False:
                    #print("First vowel found!",temp,ch)
                    firstVowelFound=True
                    str.insert(0,temp)
                    i=i+1
                elif firstVowelFound==True:
                    str.insert(0,temp)
                    i=i+1
            normWord1.append(str)
            if i in normWord1Dict.keys():
                normWord1Dict[i].append(str)
                lenNormWord1.append(len(str))
            else:
                normWord1Dict[i]=[str]
                lenNormWord1.append(len(str))
        #print("normWord1+++",normWord1)
        #print("normWord1Dict++", normWord1Dict)

        for proInst in proWord2:
            firstVowelFound = False
            # firstConsonantFound=False
            str = []
            pron = proInst
            i = 0
            for ch in pron:
                temp = ch
                lenTemp = len(temp)
                x = ''

                # chLen=len(ch)
                #print("ch-->", ch)
                if lenTemp == 3 and ch[-1].isdigit():
                    x = ch[:lenTemp - 1]
                    #print("Inside IF-->", x)
                elif lenTemp == 4 and ch[-2].isdigit():
                    x = ch[:2] + " " + ch[3]
                    #print("Inside ELIF-->", x)
                else:
                    x = ch

                if x in vowelsLst and firstVowelFound == False:
                    #print("First vowel found!", temp, ch)
                    firstVowelFound = True
                    str.insert(0, ch)
                    i = i + 1
                elif firstVowelFound == True:
                    str.insert(0, ch)
                    i = i + 1
            normWord2.append(str)
            if i in normWord2Dict.keys():
                normWord2Dict[i].append(str)
                lenNormWord2.append(len(str))
            else:
                normWord2Dict[i] = [str]
                lenNormWord2.append(len(str))
        #print("normWord2+++", normWord2)
        #print("normWord2Dict++", normWord2Dict)

        #print("lenNormWord1-->",lenNormWord1)
        #print("lenNormWord2-->", lenNormWord2)
        minWord1=min(lenNormWord1)
        minWord2=min(lenNormWord2)
        matchFound=False
        if len(normWord2)!=0 or len(normWord1)!=0:

            if minWord1<minWord2:
                #print("normWordl is less",minWord1,minWord2)
                toBeChecked=normWord1Dict[minWord1]
                #fromLst=normWord2Dict.values()
                numWords1=len(toBeChecked)
                #print("toBeChecked++",toBeChecked)
                #print("numWords1",numWords1)


                for x in toBeChecked:
                    temp=x
                    lenTemp=minWord1

                    for str in normWord2:

                        if len(str)>=lenTemp:
                            #i=0
                            tempIndex2 = 0
                            for i in range(0,lenTemp):
                                if x[i]==str[i]:
                                    tempIndex2=tempIndex2+1
                                i=i+1
                            if tempIndex2==minWord1:
                                return True



            elif minWord1>minWord2:
                #print("normWord2 is less",minWord1,minWord2)
                toBeChecked = normWord2Dict[minWord2]
                # fromLst=normWord2Dict.values()
                numWords2 = len(toBeChecked)
                #print("toBeChecked++", toBeChecked)
                #print("numWords2", numWords2)

                for x in toBeChecked:
                    temp = x
                    lenTemp = minWord2

                    for str in normWord1:

                        if len(str) >= lenTemp:
                            # i=0
                            tempIndex1 = 0
                            for i in range(0, lenTemp):
                                if x[i] == str[i]:
                                    tempIndex1 = tempIndex1 + 1
                                i = i + 1
                            if tempIndex1 == minWord2:
                                return True
            elif minWord1==minWord2:
                #print("Equal",minWord1,minWord2)
                toBeChecked = normWord1Dict[minWord1]
                # fromLst=normWord2Dict.values()
                numWords1 = len(toBeChecked)
                #print("toBeChecked++", toBeChecked)
                #print("numWords1", numWords1)

                for x in toBeChecked:
                    temp = x
                    lenTemp = minWord1

                    for str in normWord2:

                        if len(str) >= lenTemp:
                            # i=0
                            tempIndex2 = 0
                            for i in range(0, lenTemp):
                                if x[i] == str[i]:
                                    tempIndex2 = tempIndex2 + 1
                                i = i + 1
                            if tempIndex2 == minWord1:
                                return True
                toBeChecked = normWord2Dict[minWord2]
                # fromLst=normWord2Dict.values()
                numWords2 = len(toBeChecked)
                #print("toBeChecked++", toBeChecked)
                #print("numWords2", numWords2)

                for x in toBeChecked:
                    temp = x
                    lenTemp = minWord2

                    for str in normWord1:

                        if len(str) >= lenTemp:
                            # i=0
                            tempIndex1 = 0
                            for i in range(0, lenTemp):
                                if x[i] == str[i]:
                                    tempIndex1 = tempIndex1 + 1
                                i = i + 1
                            if tempIndex1 == minWord2:
                                return True
        else:
            return False



        # TODO: provide an implementation!
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        return False

    def is_limerick(self, text):


        lstLines=[x.strip() for x in text.split("\n")]
        #print ("Text-->",lstLines)

        lstLinesNew=[x for x in lstLines if len(x)!=0]
        #print("lstLinesNew-->",len(lstLinesNew),lstLinesNew)
        if(len(lstLinesNew)!=5):
            return False
        listA=[]
        listA.append(lstLinesNew[0])
        listA.append(lstLinesNew[1])
        listA.append(lstLinesNew[4])
        listB=[]
        listB.append(lstLinesNew[2])
        listB.append(lstLinesNew[3])
        #print("listA-->",listA)
        #print("listB-->", listB)
        line1A = nltk.word_tokenize(listA[0])
        line2A = nltk.word_tokenize(listA[1])
        line5A = nltk.word_tokenize(listA[2])
        line3B = nltk.word_tokenize(listB[0])
        line4B = nltk.word_tokenize(listB[1])
        #print("line1A-->", line1A)
        #print("line2A-->", line2A)
        print("line5A-->", line5A)
        #print("line3B-->", line3B)
        #print("line4B-->", line4B)

        #print("alnum test-->","prude".isalnum())
        #str=
        while(not line1A[-1].isalnum()):
            line1A=line1A[:-1]
            #str=line1A[:-1]
        while(not line2A[-1].isalnum()):
            line2A=line2A[:-1]
        while(not line5A[-1].isalnum()):
            line5A=line5A[:-1]
        while(not line3B[-1].isalnum()):
            line3B=line3B[:-1]
        while(not line4B[-1].isalnum()):
            line4B=line4B[:-1]

        #print("After removing special characters-->")
        #print("line1A-->", line1A)
        #print("line2A-->", line2A)
        #print("line5A-->", line5A)
        #print("line3B-->", line3B)
        #print("line4B-->", line4B)



        #print("Last words A-->", line1A[-1], line2A[-1], line5A[-1])
        #print("Last words B-->", line3B[-1], line4B[-1])


        LimerickDetectorInst=LimerickDetector()

        rhyme12A=LimerickDetectorInst.rhymes(line1A[-1],line2A[-1])
        #print("rhyme12A-->",rhyme12A)
        if(rhyme12A!=True):
            #print("Failing Condition rhyme12A!=True")
            return False
        rhyme25A =LimerickDetectorInst.rhymes(line2A[-1], line5A[-1])
        #print("rhyme25A-->", rhyme25A)
        if(rhyme25A!=True):
            #print("Failing Condition rhyme25A!=True")
            return False
        rhyme34B = LimerickDetectorInst.rhymes(line3B[-1],line4B[-1])
        #print("rhyme34B-->", rhyme34B)
        if(rhyme34B!=True):
            #print("Failing Condition rhyme34B!=True")
            return False
        rhyme1A3B= LimerickDetectorInst.rhymes(line1A[-1],line3B[-1])
        if(rhyme1A3B==True):
            #print("Failing Condition rhyme1A3B==True")
            return False
        rhyme2A3B= LimerickDetectorInst.rhymes(line2A[-1],line3B[-1])
        if(rhyme2A3B==True):
            #print("Failing Condition rhyme2A3B==True")
            return False
        rhyme5A3B= LimerickDetectorInst.rhymes(line5A[-1],line3B[-1])
        if(rhyme5A3B==True):
            #print("Failing Condition rhyme5A3B==True")
            return False

        rhyme1A4B= LimerickDetectorInst.rhymes(line1A[-1],line4B[-1])
        if(rhyme1A4B==True):
            #print("Failing Condition rhyme1A4B==True")
            return False
        rhyme2A4B= LimerickDetectorInst.rhymes(line2A[-1],line4B[-1])
        if(rhyme2A4B==True):
            #print("Failing Condition rhyme2A4B==True")
            return False
        rhyme5A4B= LimerickDetectorInst.rhymes(line5A[-1],line4B[-1])

        if(rhyme5A4B==True):
            #print("Failing Condition rhyme5A4B==True")
            return False

        #Checking rhymig contraint
        """
        if(rhyme12A!=True):
            return False
        elif (not LimerickDetectorInst.rhymes(line2A[-1],line5A[-1])):
            return False
        elif (not LimerickDetectorInst.rhymes(line3B[-1],line4B[-1])):
            return False
            """

        #checking syllable constraints

        line1ASyllables = 0
        line2ASyllables = 0
        line5ASyllables = 0
        line3BSyllables = 0
        line4BSyllables = 0
        lineASyllables=[]
        lineBSyllables=[]

        for word in line1A:
            if(len(word)==1 and word.isalnum()):
                syl = LimerickDetectorInst.num_syllables(word)
                line1ASyllables = line1ASyllables + syl
            elif(len(word)>1):
                syl=LimerickDetectorInst.num_syllables(word)
                line1ASyllables = line1ASyllables + syl
            #print("word+syl",word,syl)
            #line1ASyllables=line1ASyllables+syl
        lineASyllables.insert(0,line1ASyllables)
        print("line1ASyllables",line1ASyllables)
        if(line1ASyllables<4):
            #print("Failing Condition line1ASyllables<4")
            return False
        for word in line2A:
            if (len(word) == 1 and  word.isalnum()):
                syl = LimerickDetectorInst.num_syllables(word)
                line2ASyllables = line2ASyllables + syl
            elif (len(word) > 1):
                syl = LimerickDetectorInst.num_syllables(word)
                line2ASyllables = line2ASyllables + syl
            #print("word+syl",word,syl)
            #line2ASyllables=line2ASyllables+syl
        lineASyllables.insert(0,line2ASyllables)
        print("line2ASyllables",line2ASyllables)
        if(line2ASyllables<4):
            return False
        for word in line5A:
            if (len(word) == 1 and word.isalnum()):
                syl = LimerickDetectorInst.num_syllables(word)
                line5ASyllables = line5ASyllables + syl

            elif (len(word) > 1):
                syl = LimerickDetectorInst.num_syllables(word)
                line5ASyllables = line5ASyllables + syl
            #print("word+syl",word,syl)

        lineASyllables.insert(0,line5ASyllables)
        print("line5ASyllables",line5ASyllables)
        if(line5ASyllables<4):
            return False

        for word in line3B:
            if (len(word) == 1 and word.isalnum()):
                syl = LimerickDetectorInst.num_syllables(word)
                line3BSyllables = line3BSyllables + syl
            elif (len(word) > 1):
                syl = LimerickDetectorInst.num_syllables(word)
                line3BSyllables = line3BSyllables + syl
            #print("word+syl",word,syl)
            #line3BSyllables=line3BSyllables+syl
        lineBSyllables.insert(0,line3BSyllables)
        print("line3BSyllables",line3BSyllables)
        if(line3BSyllables<4):
            return False
        for word in line4B:
            if (len(word) == 1 and word.isalnum()):
                syl = LimerickDetectorInst.num_syllables(word)
                line4BSyllables = line4BSyllables + syl
            elif (len(word) > 1):
                syl = LimerickDetectorInst.num_syllables(word)
                line4BSyllables = line4BSyllables + syl
            #print("word+syl",word,syl)
            #line4BSyllables=line4BSyllables+syl
        lineBSyllables.insert(0,line4BSyllables)
        print("line4BSyllables",line4BSyllables)
        if(line4BSyllables<4):
            return False
        #print("lineASyllables",lineASyllables)
        #print("lineBSyllables", lineBSyllables)


        #print("***********")
        #lstA=copy.copy(lineASyllables.sort())
        #lstB=copy.copy(lineBSyllables.sort())
        lstA=sorted(lineASyllables)
        lstB =sorted(lineBSyllables)
        #print('lstA',lstA)
        #print('lstB', lstB)
        for a in lstA:
            for b in lstB:
                if a<b:
                    return False

        if(lstB[1]-lstB[0]>2):
            return False
        if(lstA[1]-lstA[0]>2 or lstA[2]-lstA[1]>2 or lstA[2]-lstA[0]>2):
            return False


        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
        return True


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

ld=LimerickDetector()
a = """There was a young lady one fall
Who wore a newspaper dress to a ball.
The dress caught fire
And burned her entire
Front page, sporting section and all."""
rt=ld.is_limerick(a)
print("rt+++",rt)

#if __name__ == '__main__':
# main()
