"""
python drocta ~ATH interpreter
It interprets things written in drocta ~ATH
and is written in python.
Really, I thought the name was fairly self explanatory.
Build number:10
(note:build number might not be accurate, sometimes I forget to increment it.
But I dont decrement it so its still maybe somewhat useful.
or you could just check the github versions. w/e.)
"""

import bif
import re
import pdb


def bifurcate(valueA,valueB=False):
    if(valueB):
        return bif.unbifurcate(valueA, valueB)
    else:
        return bif.bifurcate(valueA)


def matchParens(text,start,openStr,closeStr):
    count=0
    charNum=start
    firstChar=True
    while(count>0 or firstChar):
        if(charNum>=len(text)):
            #print "err:could not find match!"
            return -1
        elif(text[charNum]==closeStr):
            count=count-1
            #print "close at "+str(charNum)
        elif(text[charNum]==openStr):
            count=count+1
            #print "open at "+str(charNum)
            if(firstChar):
                firstChar=False
        charNum=charNum+1
    return charNum-1

def textToNextSemicolon(text,start=0):
    semicolonOffset=text.find(';',start)
    return text[start:semicolonOffset]

charObjs={}
def getCharObj(theChar):
    if(theChar in charObjs):
        return charObjs[theChar]
    else:
        theCharObj=bif.value_obj()
        charObjs[theChar]=theCharObj
        return theCharObj
def getStrObj(theStr):
    if(len(theStr)==0):
        return NULL_obj
    else:
        return bifurcate(getCharObj(theStr[0]),getStrObj(theStr[1:]))

def getObjStr(theObj):
    outStr=""
    theObj2=theObj
    while(theObj2.living):
        (leftObj,rightObj)=bifurcate(theObj2)
        for char in charObjs:
            if(charObjs[char]==leftObj):
                outStr+=char
                break
        theObj2=rightObj
    return outStr


funCodes={}
funCodes['HELLO']="""
print "Hello World.";"
THIS.DIE(THIS);"""
funCodes["ADD"]="""
import bluh BLAH;
BIFURCATE ARGS[A,B];
BIFURCATE [BLAH,A]ATEMP;
BIFURCATE [BLAH,B]BTEMP;
BIFURCATE ATEMP[JUNK,ATEMP];
BIFURCATE BTEMP[JUNK,BTEMP];
BIFURCATE [BLAH,NULL]C;
BIFURCATE C[JUNK,C];
~ATH(ATEMP){
BIFURCATE ATEMP[JUNK,ATEMP];
BIFURCATE [BLAH,C]C;
}
~ATH(BTEMP){
BIFURCATE BTEMP[JUNK,BTEMP];
BIFURCATE [BLAH,C]C;
}
/*
BIFURCATE [BLAH,C]CTEMP;
BIFURCATE CTEMP[JUNK,CTEMP];
~ATH(CTEMP){
BIFURCATE CTEMP[JUNK,CTEMP];
print some text;
}
print DONE!;
*/
THIS.DIE(C);
"""#NOTE:use a better addition algorithm.


NULL_obj=bif.value_obj()
NULL_obj.DIE()
def evalScript(script,inObj):
    ATHVars={}
    THIS=bif.value_obj()
    ATHVars['THIS']=THIS
    ATHVars['NULL']=NULL_obj
    ATHVars['ARGS']=inObj
    return_obj=NULL_obj

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
        elif(re.match(r'importf ([^; ]+) as ([^; ]+);',script[charNum:])!=None):
            matches=re.match(r'importf ([^; ]+) as ([^; ]+);',script[charNum:])
            importfFilename=matches.group(1)
            #print "the filename is "+importfFilename
            try:
                importfFilelink=open(importfFilename,'r')
                newFunc=importfFilelink.read(-1)
                #print newFunc
                funCodes[matches.group(2)]=newFunc
            except:
                print "could not read file "+importfFilename
            charNum=script.find(';',charNum)   
        elif(script.startswith('~ATH(',charNum)):
            closeparenOffset=script[charNum:].index(')')
            loopVar=script[charNum+5:charNum+closeparenOffset]
            loopVar=loopVar.strip(' \t\n\r')
            #print "reached ~ATH command, loopVar is "+loopVar
            if(loopVar in ATHVars):
                if(ATHVars[loopVar].living):
                    execStack.append((charNum,'{'))
                    charNum+=closeparenOffset
                    #print "loop on "+loopVar
                else:
                    #print "parenmatch jump from "+str(charNum)
                    charNum=matchParens(script,charNum,'{','}')+2
                    #print "parenmatch jumped to char:"+str(charNum)+" which was"+script[charNum]
                    #print "loopVar was "+loopVar
            else:
                print('warning/error: \"{0}\" is undefined'.format(loopVar))
        elif(script.startswith('}',charNum)):
            openingTuple=execStack.pop()
            if(openingTuple[1]=='{'):
                charNum=openingTuple[0]
            else:
                print('what are you trying to do? \"(...}\" error')
        elif(script.startswith('print ',charNum)):
            #print "print..."
            semicolonOffset=script[charNum:].index(';')
            print(script[charNum+6:charNum+semicolonOffset])
            charNum+=semicolonOffset#+6
        elif(re.match(r'PRINT2 ([^\[\];]*);',script[charNum:])!=None):
            matches=re.match(r'PRINT2 ([^\[\];]*);',script[charNum:])
            print getObjStr(ATHVars[matches.group(1)])
            charNum=script.find(';',charNum)
        elif(script.startswith('INPUT',charNum)):
            semicolonOffset=script[charNum:].index(';')
            varname=script[charNum+6:charNum+semicolonOffset]
            #print 'INPUT varname was "'+varname+'"'
            ATHVars[varname]=getStrObj(raw_input(':'))
            charNum+=semicolonOffset
        elif(re.match(r'BIFURCATE ([^\[\];]*)\[([^\[\];]*),([^\[\];]*)\];',script[charNum:])!=None):
            #print("binurcate the thing!")
            matches=re.match(r'BIFURCATE ([^\[\];]*)\[([^\[\];]*),([^\[\];]*)\];',script[charNum:])
            (ATHVars[matches.group(2)],ATHVars[matches.group(3)])=bifurcate(ATHVars[matches.group(1)])
            charNum=script.find(';',charNum)
        elif(re.match(r'BIFURCATE \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])!=None):
            matches=re.match(r'BIFURCATE \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])
            ATHVars[matches.group(3)]=bifurcate(ATHVars[matches.group(1)],ATHVars[matches.group(2)])
            charNum=script.find(';',charNum)
        elif(script.startswith('BIFFURCATE ',charNum)):
            charNum+=10
            semicolonOffset=script[charNum:].index(';')
            openSquareOffset=script[charNum:].index('[')
            closeSquareOffset=script[charNum:].index(']')
            commaOffset=script[charNum:].index(',')
            syntacticallyCorrect=True
            for offset in [openSquareOffset,closeSquareOffset,commaOffset]:
                if((offset==-1) or (offset>semicolonOffset)):
                    print("Bifurcate command malformed, char:"+str(charNum))
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
        elif(re.match(r'([0-9a-zA-Z]+)\.DIE\(([0-9a-zA-Z]*)\);',script[charNum:])!=None):#script[charNum:script[charNum:].find(';')].endswith('.DIE()')):
            matches=re.match(r'([0-9a-zA-Z]+)\.DIE\(([0-9a-zA-Z]*)\);',script[charNum:])#.group(1)
            varname=matches.group(1)
            argvarname=matches.group(2)
            if argvarname:
                #print("argvarname is " +argvarname)
                return_obj=ATHVars[argvarname]
            #print "found .DIE(); statement! Variable name is "+varname
            ATHVars[varname].DIE()
            charNum=script.find(';',charNum)
            #print varname+"killed"
        elif(script.startswith('//',charNum)):
            nextNewlinePos=script.find('\n',charNum)
            if '\r' in script[charNum:nextNewlinePos]:
                nextNewlinePos=script.find('\r',charNum)
            charNum=nextNewlinePos
        elif(script.startswith('/*',charNum)):
            charNum=script.find('*/',charNum)
        elif(script.startswith('PYDEBUG',charNum)):
            pdb.set_trace()
            charNum+=5
        elif(re.match(r'([A-Z0-9_]+) \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])!=None):
            try:
                matches=re.match(r'([A-Z0-9_]+) \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])
                funName=matches.group(1)
                #print "the function called '"+funName + "' was called."
                #print "yeah it works."
                if funName in funCodes:
                    theFuncCode=funCodes[funName]
                    sentInObject=bifurcate(ATHVars[matches.group(2)],ATHVars[matches.group(3)])
                    ATHVars[matches.group(4)]=evalScript(theFuncCode,sentInObject)
                else:
                    print "error: function called '"+funName+"' not recognized"
                charNum+=len(funName)
            except:
                print "function not recognized/ a bug in the interpreter"
                print matches#re.match(r'([A-Z0-9_]+) \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])
                print "..."
                charNum+=1
            #charNum+=1
        elif(re.match(r'([A-Z0-9_]+) ([^\[\];]*)\[([^\[\];]*),([^\[\];]*)\];',script[charNum:])!=None):
            try:
                matches=re.match(r'([A-Z0-9_]+) ([^\[\];]*)\[([^\[\];]*),([^\[\];]*)\];',script[charNum:])
                funName=matches.group(1)
                #print "the function called '"+funName + "' was called."
                #print "yeah it works."
                if funName in funCodes:
                    theFuncCode=funCodes[funName]
                    sentInObject=ATHVars[matches.group(2)]#bifurcate(ATHVars[matches.group(2)],ATHVars[matches.group(3)])
                    ATHVars[matches.group(3)],ATHVars[matches.group(4)]=bifurcate(evalScript(theFuncCode,sentInObject))
                else:
                    print "error: function called '"+funName+"' not recognized"
                charNum+=len(funName)
            except:
                print "function not recognized/ a bug in the interpreter"
                print matches#re.match(r'([A-Z0-9_]+) \[([^\[\];]*),([^\[\];]*)\]([^\[\];]*);',script[charNum:])
                print "..."
                charNum+=1
        else:
             charNum+=1
             if(charNum > len(script)):
                 THIS.DIE()
        #print script[charNum]
    return return_obj
filename=raw_input()
filelink=open(filename,'r')
script=filelink.read(-1)
result_obj=evalScript(script,NULL_obj)
raw_input("press enter to close")             
         
         
        
            
        
        
        
        
