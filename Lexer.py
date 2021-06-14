##########################################################
#         Project Deliverable: Lexer phase               #
#                   Team members:                        #
#                   DRIOUECH Saad                        #
#                LAMIRI Fatima Zahrae                    #
#                   IRAOUI Imane                         #
#                   EL AMRANI Omar                       #
##########################################################

import re
import sys
from Token import *
 #sprintf(temp, "%0*d", 4, line2-cnt); 

#dictionary that maps each lexeme to its token
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

class Lexer:
  #symbol table dictionary which is going to map each symbol to its type
  def __init__(self):
    self.symbolTableDict = {}
    #literal table list
    self.literalTable = []
    self.tokensList = list()
    self.lineNumber = 1

  #function used to scan comments in the program
  def scanComment (self,infp):
    while 1:
      c = infp.read(1)
      if not c:
        break
      else:
        if re.match("[a-zA-Z_0-9]", c):
          pass
        #if ! is found then it's either the start o the delimiter
        elif c == '!': 
          c = infp.read(1)
          #if another ! is found, then "!!" was found so the scanning ends here
          if c == '!':
            print("A comment was read")
            print("Line " , self.lineNumber , "Token" , tokensDict["!!"] , ":" , "!!")
          # tokensList.append(tokensDict["!!"])
            #we return flag=0 in case a comment was read, so that we can read the following character in the main
            return 0
    #we return flag=1 in case we read a character that's not "!", in which case we need to tokenize it in the main instead of reading the next character
    return 1

  #function used to scan a string from the file when "$" is found
  def scanString (self,c, infp):
    #variable that will hold the string
    temp = ""
    while 1:
      ch = infp.read(1)
      #if the end of file was reached we terminate the function
      if not ch:
        break
      else:
        if re.match("[a-zA-Z_0-9 ]", ch):
          temp += ch
        #if the delimiter is found we return the string
        elif ch == '$': 
          return temp

  #function used to scan numeric literals
  def scanInt(self, c, temp, infp):
    while re.match("[0-9]", c):
      #keep appending digits to the temp variable
      temp += c
      c = infp.read(1)
    #return the entire numeric literal after scanning it
    return temp, c

  def lex(self):    
    #pointer to the input file which contains the code
    infp = open("code.txt","r")
    #output file which contains the tokens and the program's output
    outfp = open("output.txt","w")
    #redirecting stdout to the output file
    sys.stdout = outfp
    #variable that helps regulate when the next character should be read
    flag=1

    c = infp.read(1)

    #loop that reads the file
    while 1:
      
      #if the flag variable is different from 1 it means we need to read the next character
      if flag != 1:
        c = infp.read(1)
        
      #if EOF is reached we terminate the loop
      if not c:
        break
      flag = 0
      #case when a space is found
      if re.match(" ", c):
        print("Space is encountered")
      #case when a new line is found
      elif re.match("\n", c):
        self.lineNumber += 1
        print("New line is encountered")
      #case when punctuation is found
      elif re.match("[;|,|:]", c):
        if(re.match("[;]",c)):
          res=' '
        print("Line" , self.lineNumber , "Token " , tokensDict[c] , " : " , c)
        token = Token(tokensDict[c], c, self.lineNumber)
        self.tokensList.append(token)

      #case when a digit is found
      elif re.match("[0-9]", c):
        #variable that is used to hold the entire numeric literal (if it has more than 1 digit)
        temp = c
        c = infp.read(1)
        #calling the scanInt function to read the numeric literal
        num, c = self.scanInt(c, temp, infp)
        #setting flag to 1 since we read an additional character at the end of the scanInt function
        flag = 1
        print("Line " , self.lineNumber , "Token" , tokensDict["LIT"] , ":" , num)
        token = Token(tokensDict["LIT"], num, self.lineNumber)
        self.tokensList.append(token)

        #case when the number designates the length of an array
        if c!=']':
          self.literalTable.append(num)

      #this part of the code checks if the current character is an operator
      elif re.match("[=|<|>|!|+|*|/|%|-]", c):
        #cawe when a minus or plus is found
        if c in ("+", "-"):
          temp = c
          c = infp.read(1)
          #if EOF is reached we break
          if not c:
            break
          else:
            #case when the character that follows is space means that the '-|+'  is an operator
            if c == " ":
              if temp == "+":
                print("Line" , self.lineNumber , "Token" , tokensDict["+"] , ": +")
                token = Token(tokensDict["+"], "+", self.lineNumber)
                self.tokensList.append(token)
              elif temp == "-":
                print("Line" , self.lineNumber , "Token" , tokensDict["-"] , ": -")
                token = Token(tokensDict["-"], "-", self.lineNumber)
                self.tokensList.append(token)
            #case when the character that follows is a numnber means that the '-|+' is a sign
            elif re.match("[0-9]", c):
              temp += c
              c = infp.read(1)
              if not c:
                break
              else:
                num, c = self.scanInt(c, temp, infp)
                flag = 1
                print("Line" , self.lineNumber , "Token" , tokensDict["LIT"] , ":", num)
                token = Token(tokensDict["LIT"], num, self.lineNumber)
                self.tokensList.append(token)

        #if the characters is an equal sign 
        elif c == '=':
          #we check the character after it
          c = infp.read(1)
          #break if we reach EOF
          if not c:
            break
          #if the character after "=" is ">" then it's a comparison sign
          else:
            if c == '>':
              print("Line " , self.lineNumber , "Token" , tokensDict["=>"] , ":" , "=>")
              token = Token(tokensDict["=>"], "=>", self.lineNumber)
              self.tokensList.append(token)
            #otherwise it's just an equal sign
            else:
              flag = 1
              print("Line " , self.lineNumber , "Token" , tokensDict["="] , ":" , "=")
              token = Token(tokensDict["="], "=", self.lineNumber)
              self.tokensList.append(token)
        #if the character read is "!"
        elif c == '!':
          #we check the following character to differentiate between "!=" and "!!"
          c = infp.read(1)
          if not c:
            break
          else:
            #if it's followed by an equal sign then it's treated as "!="
            if c == '=':
              print("Line " , self.lineNumber , "Token" , tokensDict["!="] , ":" , "!=")
              token = Token(tokensDict["!="], "!=", self.lineNumber)
              self.tokensList.append(token)
            #if it's followed by another "!" then it's a comment
            elif c == '!':
              print("Line " , self.lineNumber , "Token" , tokensDict["!!"] , ":" , "!!")
              #tokensList.append(tokensDict["!!"])
              #we scan the entire comment and we set flag according to the return value
              flag = self.scanComment(infp)
            else:
              flag = 1
              print("error\n")
        #if the character is "<", we check the next character to see whether the operator is "<=" or "<"
        elif c == '<':
          c = infp.read(1)
          if c == '=':
            print("Line " , self.lineNumber , "Token" , tokensDict["<="] , ":" , "<=")
            token = Token(tokensDict["<="], "<=", self.lineNumber)
            self.tokensList.append(token)
          else:
            print("Line " , self.lineNumber , "Token" , tokensDict["<"] , ":" , "<")
            token = Token(tokensDict["<"], "<", self.lineNumber)
            self.tokensList.append(token)
            flag = 1
        #if the character is ">", we check the next character to see whether the operator is ">=" or ">"
        elif c == '>':
          c = infp.read(1)
          if c == '=':
            print("Line ",self.lineNumber , "Token" , tokensDict[">="] , ":" , ">=")
            token = Token(tokensDict[">="], ">=", self.lineNumber)
            self.tokensList.append(token)
          else:
            print("Line " , self.lineNumber , "Token" , tokensDict[">"] , ":" , ">")
            token = Token(tokensDict[">"], ">", self.lineNumber)
            self.tokensList.append(token)
            flag = 1
        
        else:
          print("Line " ,  self.lineNumber , "Token" , tokensDict[c] , ":" , c)
          token = Token(tokensDict[c], c, self.lineNumber)
          self.tokensList.append(token)
          
      #this checks for user identifiers and reserved words
      elif re.match("[a-zA-Z_]", c):
        #variable used to hold the entire string read
        temp = c
        c = infp.read(1)
        #while the character being read is alphanumeric, we keep reading and appending to temp
        while re.match("[a-zA-Z_0-9]", c):
          temp += c
          c = infp.read(1)
        #setting the flag to 1 since we read an additional character at the end of the loop
        flag = 1

        #if the string is a logical operator
        if temp in ("MACHI", "WLA", "O"):
          print("Line " ,  self.lineNumber , "Token" , tokensDict[temp] , ":" , temp )
          token = Token(tokensDict[temp], temp, self.lineNumber)
          self.tokensList.append(token)

        #if the string is a reserved word
        elif temp in ("hbess", "ramz", "aadad", "tabita", "mahed", "rejaa", "walou", "ila","ilaghalat", "bda", "sali", "qra", "tebaa","mouhima","dalla"):
          print("Line " , self.lineNumber , "Token" , tokensDict[temp] , ":" , temp)
          token = Token(tokensDict[temp], temp, self.lineNumber)
          self.tokensList.append(token)
          res = temp
        #case when the character is "*" or "/" or "%"
        else:
          #if the string read is a user identifier we tokenize it as an ID
          print("Line " ,  self.lineNumber , "Token" , tokensDict["ID"] , ":" , temp)
          token = Token(tokensDict["ID"], temp, self.lineNumber)
          self.tokensList.append(token)
          #appending the user identifier to the symbol table after its declaration
          if res == "aadad" or res == "ramz" or res == "tabita":
            #if it's a user identifier
            if c!='(':
              if(temp not in self.symbolTableDict and res!=' '):
                print(temp)
                self.symbolTableDict[temp] = res
            #if it's a function name
            else:
              self.symbolTableDict[temp] = "function"

      #this part of the code checks if the current character is a single quote which marks the begining of a character literal  
      elif c == "'":
        c = infp.read(1)
        #check if the charcter scanned is a an alpahbet, number, or underscore
        if re.match("[a-zA-Z_0-9]", c):
          #check i
          temp = c
          c = infp.read(1)
          #update literal and symbol table
          if not c:
            break
          #this checks if we reached the delimiter of character literals 
          elif c == "'":
            print("Line " ,  self.lineNumber , "Token" , tokensDict["LIT"] , ":" , temp)
            token = Token(tokensDict["LIT"], temp, self.lineNumber)
            self.tokensList.append(token)
            #appending the character to the literal table
            self.literalTable.append(temp)

      #this part of the code checks if the current character is '$' which marks the begining of a string literal
      elif c == '$':  
        #scanStrings return the string literal
        string = self.scanString(c, infp)
        if string is not None:
          c = infp.read(1)
          flag = 1 
          print("Line " ,  self.lineNumber , "Token" , tokensDict["LIT"] , ":" , string)
          token = Token(tokensDict["LIT"], string, self.lineNumber)
          self.tokensList.append(token)
          if c != ')': 
            #appending the string to the literal table if it's not followed by ")", i.e if it's not a string inside a "tebaa"(print) statement
            self.literalTable.append(string)
        else:
          print("couldn't find the delimiter $")

      elif c in ("(", ")", "[", "]"):
        print("Line " ,  self.lineNumber , "Token" , tokensDict[c] , ":" , c)
        token = Token(tokensDict[c], c, self.lineNumber)
        self.tokensList.append(token)
      else:
        print("Character not supported by the language!")


    #these following lines could be used to print the contents of both the literal table and the symbol table at the end of the file (need to be uncommented)
    print("\n\n--Symbol Table:\n")
    for i in self.symbolTableDict:
      print(i, self.symbolTableDict[i])

    #for i in literalTable:
    #  print(i)

    print("\n\n--Tokens List:\n")
    for i in self.tokensList:
      print(i.token_name, i.token_num, i.token_line)

    #print(self.tokensList)
