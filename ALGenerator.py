from Token import *
import sys
import itertools

varflag = 0
labelcnt = 0
cntcond = 1
labelcntloop = 0
endloopcnt =0
cntloop = 1
endcnt = 1

tokensDict = {
  "aadad" : "#0",
  "ramz" : "#1",
  "&" : "#2",
  "[" : "#3",
  "]" : "#4",
  "(" : "#5",
  ")" : "#6",
  ";" : "#7",
  "," : "#8",
  ":" : "#9",
  "!!" : "#10",
  "MACHI" : "#11",
  "WLA" :"#12",
  "O" : "#13",
  "hbess" : "#14",
  "tabita" : "#15",
  "mahed" : "#16",
  "rejaa" : "#17",
  "walou" : "#18",
  "ila" : "#19", 
  "ilaghalat" : "#20",
  "bda" : "#21",
  "sali" : "#22",
  "=>" : "#23",
  "<" : "#24",
  ">" : "#25",
  "=" : "#26",
  "<=" : "#27",
  ">=" : "#28",
  "!=" : "#29",
  "+" : "#30",
  "-" : "#31",
  "*" : "#32",
  "/" : "#33",
  "%" : "#34",
  "ID" : "#35",
  "$" : "#36",
  "tebaa" : "#37",
  "qra" : "#38",
  "mouhima" : "#39",
  "LIT" : "#40",
   "dalla": "#41"  
}

class ALGenerator:
  def __init__ (self, tokensList):
    self.tokensList = tokensList
  
  def instantiate (self):
    self.tokensList_cycle = itertools.cycle(self.tokensList)
    self.current_token = next(self.tokensList_cycle)
    f = open("ALoutput.txt", "w")
    sys.stdout = f
    
  def generateAssembly (self):
    global varflag
    global labelcnt
    global cntcond
    global endloopcnt
    global labelcntloop
    global cntloop
    global endcnt

    if self.current_token.token_name == "mouhima":
      #iterating until we find "bda", then taking the next token when we get out of the loop
      while self.current_token.token_name != "bda":
        self.current_token = next(self.tokensList_cycle)
      
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()

    elif (self.current_token.token_name == "aadad"):
      #iterating while we are still declaring variables
      while self.current_token.token_name != ';':
        self.current_token = next(self.tokensList_cycle)
        print('DEF ' + self.current_token.token_name + ' 0000')
        #getting the next token
        self.current_token = next(self.tokensList_cycle)

      #moving on to the next token after finding ';''
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()

    #implementing READ
    elif (self.current_token.token_name == "qra"):
      #if read was the first statement in the code after variable declarations then print the seperatror (between data and code)
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')
      #reading the left paranthesis
      self.current_token = next(self.tokensList_cycle)
      #reading the variable inside 'qra'
      self.current_token = next(self.tokensList_cycle)
      print('READ ' + self.current_token.token_name + ' 0000')
      #moving on to read ) which is after 'qra'
      self.current_token = next(self.tokensList_cycle)
      #reading the semicolon
      self.current_token = next(self.tokensList_cycle)
      #getting the next token after ;
      self.current_token = next(self.tokensList_cycle)
      #recursively calling the function
      self.generateAssembly()

    elif (self.current_token.token_name == "tebaa"):
      #if print was the first statement in the code after variable declarations then print the seperatror (between data and code)
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')
      #reading the left paranthesis
      self.current_token = next(self.tokensList_cycle)
      #reading the variable inside 'qra'
      self.current_token = next(self.tokensList_cycle)
      print('PRNT ' + self.current_token.token_name + ' 0000')
      #moving on to read ) which is after 'qra'
      self.current_token = next(self.tokensList_cycle)
      #reading the semicolon
      self.current_token = next(self.tokensList_cycle)
      #getting the next token after ;
      self.current_token = next(self.tokensList_cycle)
      #recursively calling the function
      self.generateAssembly()
      
    elif (self.current_token.token_num == tokensDict["ID"] or self.current_token.token_num == tokensDict["LIT"]):
      #if assignment expression was the first statement in the code after variable declarations then print the seperatror (between data and code)
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')
        
      #getting the firts element of the left handside
      x = self.current_token.token_name
      #getting the next element to check whether the left handside of the assignment is an expression or a single value 
      self.current_token = next(self.tokensList_cycle)
      #checking if the left handside of the assignment is an expression
      if(self.current_token.token_name == '+' or self.current_token.token_name == '-' or self.current_token.token_name == '/' or self.current_token.token_name == '*'):
        #storing the operator
        op = self.current_token.token_name
        self.current_token = next(self.tokensList_cycle)
        #storing the second operand
        y = self.current_token.token_name

        #case of addition
        if(op=='+'):
          print('ADD '+x+' '+y)
        #case of substraction
        elif (op=='-'):
          print('SUB '+x+' '+y)
        #case of multiplication
        elif (op=='*'):
          print('MUL '+x+' '+y)
        #case of division
        elif (op=='/'):
          print('DIV '+x+' '+y)
        self.current_token = next(self.tokensList_cycle)
        #make sure that the next token corresponds to assignment operator
        if(self.current_token.token_num == tokensDict["=>"]):
          self.current_token = next(self.tokensList_cycle)          
          print("MOV ACC "+ self.current_token.token_name)
      
      #if the left hand sinde of the assignment statement was not an expression
      elif(self.current_token.token_num == tokensDict["=>"]):
        self.current_token = next(self.tokensList_cycle)
        #before generating the corresponding AL code, check whteher it corresponds to an assignment statement used with literal values or 
        if(x.isdigit()):
          print("MOV 000"+x+ ' ' +self.current_token.token_name)
        else:
          print("MOV "+x+ ' ' +self.current_token.token_name)

      self.current_token = next(self.tokensList_cycle)
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
    
    #case of if statement
    elif(self.current_token.token_name == "ila"):
      #if assignment expression was the first statement in the code after variable declarations then print the seperatror (between data and code)
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')

      #getting left paranthesis
      self.current_token = next(self.tokensList_cycle)
      #getting the left handside of the comparison statement
      self.current_token = next(self.tokensList_cycle)
      op1 = self.current_token.token_name
      #casting it to a string
      sop1 = str(op1)
      #gettig the comparison operator
      self.current_token = next(self.tokensList_cycle)
      ope = self.current_token.token_name
      #getting the right hand side of the comparsion statement
      self.current_token = next(self.tokensList_cycle)
      op2 = self.current_token.token_name
      #casting it to a string
      sop2 = str(op2)
      #case the operator is !=
      if(ope == "!="):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop2+" 0000")
        print("EQU "+sop1+" CL"+ str(labelcnt))
        labelcnt = labelcnt + 1
      #case the operator is =
      elif(ope == "="):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop2+" 0000")
        print("NEQU "+sop1+" CL"+str(labelcnt))
        labelcnt = labelcnt + 1
      #case the operator is >
      elif(ope == ">"):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop1+" 0000")
        print("GTE "+ sop2 + " CL"+str(labelcnt))
        labelcnt = labelcnt + 1
      #case the operator  is <
      elif(ope == "<"):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop2+" 0000")
        print("GTE "+sop1+" cL"+str(labelcnt))
        labelcnt = labelcnt + 1
      #case the operator  is >=
      elif(ope == ">="):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop2+ " 0000")
        print("SLT "+sop1+" CL"+str(labelcnt))
        labelcnt = labelcnt + 1
      #case the operator  is <=
      elif(ope == "<="):
        #generate the corresponding assembly code and increment the counter index of the labels of the conditions (which is a global variable)
        print("MOV "+sop1+" 0000")
        print("SLT "+sop2+" CL"+str(labelcnt))
        labelcnt = labelcnt + 1
      #getting the right paranthesis
      self.current_token = next(self.tokensList_cycle)
      #getting the colon
      self.current_token = next(self.tokensList_cycle)
      #getting the next token to recurse based on it
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
      #when we get back to the end of if statement we get the next token to recurse on it
      self.current_token = next(self.tokensList_cycle)
      #before recursing, we need to assign the label of the end of if statment
      temp = labelcnt - cntcond
      print("ASG CL"+str(temp)+" 0000")
      cntcond += 1
      self.generateAssembly()
    
    #case of else
    elif(self.current_token.token_name == "ilaghalat"):
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')
      #getting the colon
      self.current_token = next(self.tokensList_cycle)
      #getting the next token to recurse on it
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
    
    #case of while loop
    elif(self.current_token.token_name == "mahed"):
      #if assignment expression was the first statement in the code after variable declarations then print the seperatror (between data and code)
      if varflag == 0:
        varflag = 1
        print('+99 9999 9999')
      #getting the left paranthesis
      self.current_token = next(self.tokensList_cycle)
      #getting the left handside of the comparison statement
      self.current_token = next(self.tokensList_cycle)
      sop1 = str(self.current_token.token_name)
      self.current_token = next(self.tokensList_cycle)
      #getting the  comparison operator
      sope = str(self.current_token.token_name)
      self.current_token = next(self.tokensList_cycle)
      #getting the left handside of the comparison statement
      sop2 = str(self.current_token.token_name)
      #case the operator is !=
      if(sope == "!="):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop2+" 0000")
        print("EQU "+sop1+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #case the operator is =
      elif(sope == "="):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop2+" 0000")
        print("NEQU "+sop1+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #case the operator is >
      elif(sope == ">"):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop1+" 0000")
        print("GTE "+sop2+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #case the operator is <
      elif(sope == "<"):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop2+" 0000")
        print("GTE "+sop1+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #case the operator is >=
      elif(sope == ">="):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop2+ " 0000")
        print("SLT "+sop1+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #case the operator is <=
      elif(sope == "<="):
        #generate the corresponding assembly code and increment the counter index of the labels of the start (LL) and end (EL) of loops (which are global variables)
        print("MOV "+sop1+" 0000")
        print("SLT "+sop2+" EL"+ str(endloopcnt))
        endloopcnt = endloopcnt + 1
        print("ASG LL"+str(labelcntloop)+" 0000")
        labelcntloop = labelcntloop + 1
      #getting the left paranthesis
      self.current_token = next(self.tokensList_cycle)
      #getting the right paranthesis
      self.current_token = next(self.tokensList_cycle)
      #getting the next token to recurse based on it
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
      temp = labelcntloop - cntloop
      #the following code generate the assembly code for assigning the end of the loop label and jumping to the start of the loop in the case the condition still holds. It does so depending on 
      if(temp == 0):
        cntloop = 1
      if(sope == "!="):
        print("MOV "+sop2+" 0000")
        print("NEQU "+sop1+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      elif(sope == "="):
        print("MOV "+sop2+" 0000")
        print("EQU "+sop1+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      elif(sope == ">"):
        print("MOV "+sop1+" 0000")
        print("SLT "+sop2+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      elif(sope == "<"):
        print("MOV "+sop2+" 0000")
        print("SLT "+sop1+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      elif(sope == ">="):
        print("MOV "+sop2+ " 0000")
        print("GTE "+sop1+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      elif(sope == "<="):
        print("MOV "+sop1+" 0000")
        print("GTE "+sop2+" LL"+ str(temp))
        cntloop = cntloop + 1
        temp = endloopcnt - endcnt
        print("ASG EL"+str(temp)+" 0000")
        endcnt = endcnt + 1
      self.current_token = next(self.tokensList_cycle)
      self.generateAssembly()
    elif self.current_token.token_name == "sali":
      print("HALT 0000 0000")
      print("+99 9999 9999")