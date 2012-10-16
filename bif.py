"""
python drocta ~ATH interpreter
It interprets things written in drocta ~ATH
and is written in python.
Really, I thought the name was fairly self explanatory.

This file handles Bifurcation, reverse Bifurcation, and .DIE()
It creates the function for modifying values. (not the variables, the values)
"""

allValueObjs=[]

class value_obj:
    def __init__(self,parts=()):
        self.parts=parts
        self.formsLeftOf=[]
        self.formsRightOf=[]
        self.whichHalve=(0,0)#left half is (1,0), right half is (0,1)
        self.living=True
    def bifurcate(self):
        if(not self.parts):
            leftHalf=value_obj()
            leftHalf.formsLeftOf.append(self)
            leftHalf.whichHalve=(1,0)
            rightHalf=value_obj()
            rightHalf.formsRightOf.append(self)
            rightHalf.whichHalve=(0,1)
            self.parts=(leftHalf,rightHalf)
        return self.parts
    def DIE(self):
        self.living=False

def bifurcate(value):
    if(not value.parts):
        leftHalf=value_obj()
        leftHalf.formsLeftOf.append(value)
        leftHalf.whichHalve=(1,0)
        rightHalf=value_obj()
        rightHalf.formsRightOf.append(value)
        rightHalf.whichHalve=(0,1)
        value.parts=(leftHalf,rightHalf)
    return value.parts

def unbifurcate(valueA,valueB):
    for value in valueA.formsLeftOf:
        if(value in valueB.formsRightOf):
            return value
    combined=value_obj((valueA,valueB))
    valueA.formsLeftOf.append(combined)
    valueB.formsRightOf.append(combined)
    return combined
