def matchParens(text,start,openStr,closeStr):
    count=0
    charNum=start
    firstChar=True
    while(count>0 or firstChar):
        if(charNum>=len(text)):
            print "err:could not find match!"
            return -1
        elif(text[charNum]==closeStr):
            count=count-1
            print "close at "+str(charNum)
        elif(text[charNum]==openStr):
            count=count+1
            print "open at "+str(charNum)
        charNum=charNum+1
        if(firstChar):
            firstChar=False
    return charNum-1
