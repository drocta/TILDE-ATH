"""
python drocta ~ATH interpreter
It interprets things written in drocta ~ATH
and is written in python.
Really, I thought the name was fairly self explanatory.
"""

import bif

def bifurcate(valueA,valueB=False):
    if(valueB):
        return bif.unbifurcate(valueA, valueB)
    else:
        return bif.bifurcate(valueA)

def matchParens(text,start,openStr,closeStr):
    count=1
    searchChar=text.find(openStr,start)
    while(count>0):
        nextOpen=text.find(openStr,searchChar)
        nextClose=text.find(closeStr,searchChar)
        if(nextClose==-1):
            return searchChar
        if(nextOpen==-1):
            nextOpen=nextClose+1
        if(nextClose<=nextOpen):
            count-=1
            searchChar=nextClose+1
            #print "close"
        else:#nextClose>nextOpen
            count+=1
            searchChar=nextOpen+1
            #print "open"+str(count)+"searchChar:"+str(searchChar)
    return searchChar

def textToNextSemicolon(text,start=0):
    semicolonOffset=text.find(';',start)
    return text[start:semicolonOffset]

ATHVars={}
THIS=bif.value_obj()
ATHVars['THIS']=THIS
filename=raw_input()
filelink=open(filename,'r')
script=filelink.read(-1)

"""
lines=script.explode("\n")
lineCount=len(lines)
lineNum=0
"""

charNum=0

execStack=[]

while(THIS.living):
    if(False):
        pass
    elif(script.startswith('import ',charNum)):
        semicolonOffset=script[charNum:].index(';')
        importStatementStr=script[charNum:charNum+semicolonOffset]
        importStatementList=importStatementStr.split(' ')
        if(importStatementList[-1] not in ATHVars):
            ATHVars[importStatementList[-1]]=bif.value_obj()
        charNum+=semicolonOffset
    elif(script.startswith('~ATH(',charNum)):
        closeparenOffset=script[charNum:].index(')')
        loopVar=script[charNum+5:charNum+closeparenOffset]
        loopVar=loopVar.strip(' \t\n\r')
        if(loopVar in ATHVars):
            if(ATHVars[loopVar].living):
                execStack.append((charNum,'{'))
                charNum+=closeparenOffset
                #print "loop on "+loopVar
            else:
                charNum=matchParens(script,charNum,'{','}')
                print "jumped to char:"+str(charNum)+" which was"+script[charNum-1]
                print "loopVar was "+loopVar
        else:
            print "warning/error: \""+loopVar+"\" is undefined"
    elif(script.startswith('}',charNum)):
        openingTuple=execStack.pop()
        if(openingTuple[1]=='{'):
            charNum=openingTuple[0]
        else:
            print "what are you trying to do? \"(...}\" error"
    elif(script.startswith('print ',charNum)):
        #print "print..."
        semicolonOffset=script[charNum:].index(';')
        print script[charNum+6:charNum+semicolonOffset]
        charNum+=semicolonOffset#+6
    elif(script.startswith('BIFURCATE ',charNum)):
        charNum+=10
        semicolonOffset=script[charNum:].index(';')
        openSquareOffset=script[charNum:].index('[')
        closeSquareOffset=script[charNum:].index(']')
        commaOffset=script[charNum:].index(',')
        syntacticallyCorrect=True
        for offset in [openSquareOffset,closeSquareOffset,commaOffset]:
            if((offset==-1) or (offset>semicolonOffset)):
                print "Bifurcate command malformed, char:"+str(charNum)
                syntacticallyCorrect=False
                break
        if(syntacticallyCorrect):
            if(openSquareOffset==0):
                leftHalf=script[charNum+openSquareOffset+1:charNum+commaOffset]
                rightHalf=script[charNum+commaOffset+1:charNum+closeSquareOffset]
                combinedName=script[charNum+closeSquareOffset+1:charNum+semicolonOffset]
                ATHVars[combinedName]=bifurcate(ATHVars[leftHalf],ATHVars[rightHalf])
            else:
                toSplitName=script[charNum:charNum+openSquareOffset]
                leftHalf=script[charNum+openSquareOffset+1:charNum+commaOffset]
                rightHalf=script[charNum+commaOffset+1:charNum+closeSquareOffset]
                (ATHVars[leftHalf],ATHVars[rightHalf])=bifurcate(ATHVars[toSplitName])
    elif(".DIE()" in textToNextSemicolon(script,charNum)):#script[charNum:script[charNum:].find(';')].endswith('.DIE()')):
         varname=textToNextSemicolon(script,charNum)#script[charNum:script[charNum:].find(';')]
         varname=varname[:-6]
         varname=varname.split(' ')[-1]
         varname=varname.split('\n')[-1]
         ATHVars[varname].DIE()
         charNum=script.find(';',charNum)
         #print varname+"killed"
    else:
         charNum+=1
         if(charNum > len(script)):
             THIS.DIE()
    #print script[charNum]
             
         
         
        
            
        
        
        
        
