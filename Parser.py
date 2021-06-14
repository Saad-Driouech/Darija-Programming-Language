import itertools
import re
from Token import *
import sys

#a dictionary that maps each lexeme to its corresponding token number
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

funct_parameters=["start"]
current_funct="non"
current_ID="xx"
outp="yy"
curr_type="tt"
cond=0
cond_type="xx"
qraOrTebaa=0
parametersCy=itertools.cycle(funct_parameters)
error_free=1
#Class used to represent the nodes in the parse tree
class Node:
  def __init__(self, value):
    self.node_value = value
    self.nodes = list()

  def makeTree(self, value):

    if isinstance(value, Node):
      self.nodes.append(value)
    else:
      self.nodes.append(Node(value))

  #function to print the entire parse tree
  def generate_tree(self, level=0):
    if(self.node_value != None):
      if isinstance(self.node_value, Token):
        print('\t' * level + repr(self.node_value.token_name))
      else:
        print ('\t' * level + repr(self.node_value))
    #iterate over the children of the node and increment the level with each recursive call
    for child in self.nodes:
        child.generate_tree(level+1)

class Parser:

  def __init__ (self, tokensList,symbolTable):

    self.root = None
    self.tokensList = tokensList
    self.symbolTable=symbolTable
    self.tokensList_cycle = itertools.cycle(self.tokensList)
    self.current_token = next(self.tokensList_cycle)
    self.py_code = ''
    

  def parse(self):
    global error_free
    #initializes the root by calling the function createTree()
    root = self.createTree()
    outfp = open("generatedCode.txt","w")
    sys.stdout = outfp
    if(error_free==1):
      self.generateCode (root)
      print("Code generated from the parse tree :"+'\n\n')
      print(self.py_code)
      self.py_code =' '
      outfp=open("parsetree.txt","w")
      sys.stdout = outfp
      root.generate_tree()
      
      

  def generateCode (self, node):
    if node != None:
      #iterates over the children of the node
      for child in node.nodes:
        #recursively calls itself until it finds a node with no children, i.e a leaf
        self.generateCode(child)
        #condition to check if the node is a leaf
        if len(child.nodes)==0:
          if child.node_value!=None:
            #if the node_value is a token and not a string
            if isinstance (child.node_value, Token):
              #for code organization purposes, whenever bda, : or ; is found go back in line
              if child.node_value.token_name == 'bda'or child.node_value.token_name == ':' or child.node_value.token_name == ";" or  child.node_value.token_name == "sali" :
                if child.node_value.token_name == 'bda':
                  self.py_code += '\n'+ child.node_value.token_name + '\n'
                elif child.node_value.token_name == 'sali':
                  self.py_code += child.node_value.token_name + '\n\n'
                else:
                  self.py_code += child.node_value.token_name + '\n'
              else:
                self.py_code += child.node_value.token_name + ' '
            #if the node value is a string then append it directly
            else:
              self.py_code += child.node_value
  #function that creates the tree initially by calling program()          
  def createTree(self):
    self.root = self.program()
    
    #handle error thingy
    return self.root

  def program(self):
    #sets the tree root to program to designate the start of this subtree
    root = Node("PROGRAM")
    #appends the constants, declarations and mouhima subtrees to the tree
    root.makeTree(self.constants())
    root.makeTree(self.varDeclarations())
    root.makeTree(self.funDefinitions(root))
    root.makeTree(self.mouhima())
    return root

  def constants(self):
    global error_free
    root = Node("CONSTANTS")
    flag = 0
    #as long as we are declaring constants, keep looping
    while(self.current_token.token_num == tokensDict["tabita"]):
      flag = 1
      #append the token to the subtree
      root.makeTree(self.current_token)
      c = next(self.tokensList_cycle)
      #if we find an identifier, we check if there's a literal after it and we append it
      if(c.token_num == tokensDict["ID"]):
        root.makeTree(c)
        c = next(self.tokensList_cycle)
        if(c.token_num == tokensDict["LIT"]):
          root.makeTree(c)
        else: 
          #if the literal is not found
          print("error at line,",self.current_token.token_line,"expected a literal")
          error_free=0
      
          break
      else:
          #if the identifier is not found
          print("error at line,",self.current_token.token_line,"expected an identifier after 'tabita'")
          error_free=0
          break
      #move on to the next token
      self.current_token = next(self.tokensList_cycle)
    #if we don't find a constant declaration return a null root
    if (flag!=1):
      return None

    return root
  #acceptor for variable declarations
  def varDeclarations(self):
    flag=0
    #subroot for declarations
    root = Node("DECLARATIONS")
    while(self.current_token.token_num== tokensDict["&"] or self.current_token.token_num == tokensDict["aadad"] or self.current_token.token_num == tokensDict["ramz"]):
      flag=1
      #append variable types to the subtree
      root.makeTree(self.varType())
      #append variables to the subtree
      root.makeTree(self.variables())

    #if no variable declaration is found return a null root
    if flag==0:
      return None
    return root

  #acceptor for variable types
  def varType(self):
    root = Node("VARTYPE")
    if(self.current_token.token_num != tokensDict["&"]):
      #append stype to the vartype subtree
      root.makeTree(self.sType())
      #append structured type to the vartype subtree
      root.makeTree(self.structured())
    else:
      #if & is found it means address type so it calls the corresponding acceptor and appends it to the tree
      root.makeTree(self.address())
    return root

  #simple type acceptor
  def sType(self):
    global error_free
    root = Node("STYPE")
    if(self.current_token.token_num == tokensDict["aadad"] or self.current_token.token_num == tokensDict["ramz"]):
      #appending the token to the subtree and moving on to the next token
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
    else:
      #if some lexeme other than aadad and ramz is found
      error_free=0
      print("wrong type at line", self.current_token.token_line)
    return root

  #structured acceptor
  def structured(self):
    global error_free
    root = Node("STRUCTURED")
    #if opening bracket is found, calls expression as per the BNF
    if(self.current_token.token_num == tokensDict["["]):
      root.makeTree(self.expression())
      #if closing bracket is found append it to the tree and move to the next token
      if(self.current_token.token_num == tokensDict["]"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
      else:
        error_free=0
        #error if no closing bracket is found
        print("ERROR, expected a closing bracket ']' at line", self.current_token.token_line)
    #if no structured type declaration is found return a null root
    else:
      return None
    return root

  #acceptor for address type
  def address(self):
    root = Node("ADDRESS")
    self.current_token = next(self.tokensList_cycle)
    #calls the stype acceptor 
    root.makeTree(self.sType())
    return root

  #variables acceptor
  def variables(self):
    global error_free
    root = Node("VARIABLES")
    #if an identifier is found, aooend it and check if its followed by a bracket or a column
    while(self.current_token.token_num == tokensDict["ID"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      #if something other than column or opening bracket is found then exit the loop since it marks the end of the declarations
      if(self.current_token.token_num != tokensDict[","] and self.current_token.token_num != tokensDict["["] ):
        break
      #if an opening bracket is found then move to the next token and it checks if contains a literal or a number
      elif(self.current_token.token_num == tokensDict["["]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        if(self.current_token.token_num == tokensDict["LIT"] and re.match("[0-9]", self.current_token.token_name)  ):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          #if a closing bracket is found it marks the end of the structured type, append it to the tree and move to the next token
          if(self.current_token.token_num == tokensDict["]"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          #if no closing bracket is found after the opening bracket and literal
          else:
            error_free=0
            print("expected a closing bracket ']' at line", self.current_token.token_line)
        #if something other than a literal or a number is found between brackets
        else:
          error_free=0
          print("expected a number between brackets", self.current_token.token_num)
      #append token if column is found after a declaration
      if(self.current_token.token_num == tokensDict[","]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
    #if semicolumn is found this marks the end of the declaration
    if(self.current_token.token_num == tokensDict[";"]):
      root.makeTree(self.current_token)
    #if no semicolumn is found after the declaration
    else:
      error_free=0
      print("expected ; after variables at line", self.current_token.token_line)
    self.current_token = next(self.tokensList_cycle)
    return root

  #acceptor for mouhima
  def mouhima(self):
    global error_free
    root = Node("MOUHIMA")
    if(self.current_token.token_num == tokensDict["mouhima"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      #checking for opening parenthesis after mouhima
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        #checking for closing parenthesis after it
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          #checking for bda after mouhima()
          if(self.current_token.token_num == tokensDict["bda"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            #calling statements if bda is found
            root.makeTree(self.statements())
            #checking for sali after finishing the statements
            if(self.current_token.token_num == tokensDict["sali"]):
                root.makeTree(self.current_token)
            else:
                error_free=0
                print("error, expected 'sali' at the end of 'Mouhima'")
          else:
            error_free=0
            print("error, expected 'bda' at line", self.current_token.token_line)
        else: 
          error_free=0
          print("error, expected closing parentheses at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected opening parrentheses at line ", self.current_token.token_line)
    #error if no mouhima is found
    else: 
      error_free=0
      print("error, expected mohima at line ", self.current_token.token_line)   
    return root   

  #function definitions acceptor
  def funDefinitions(self, root2):
    global funct_parameters
    global error_free
    root = Node("FUNCTION")
    Out=''
    # checking if the first element if function definition is the reserved word "dalla"
    if(self.current_token.token_num == tokensDict["dalla"]):
      funct_parameters.append('dalla')
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      # checking that the element after dalla is the type of the output of the function
      if(self.current_token.token_num == tokensDict["aadad"] or self.current_token.token_num == tokensDict["ramz"]):
        Out=self.current_token.token_name
        root.makeTree(self.sType())
        #checking for the name of the function 
        if(self.current_token.token_num == tokensDict["ID"]):
          funct_parameters.append(self.current_token.token_name)
          #appending to the out type to the funct_parameters global list, to be used later for type checking in the function calls
          if(Out!=''):
                funct_parameters.append('Output')
                funct_parameters.append(Out)
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          #checking for the parenthesis 
          if(self.current_token.token_num == tokensDict["("]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            #calls the acceptor 'parameters' 
            root.makeTree(self.parameters())
            funct_parameters.append("EndOfFunctionParam")
            if(self.current_token.token_num == tokensDict[")"]):
              root.makeTree(self.current_token)
              self.current_token = next(self.tokensList_cycle)
              if(self.current_token.token_num == tokensDict["bda"]):
                root.makeTree(self.current_token)
                self.current_token = next(self.tokensList_cycle)
                root.makeTree(self.statements())
                if(self.current_token.token_num == tokensDict["sali"]):
                  root.makeTree(self.current_token)
                  self.current_token = next(self.tokensList_cycle)
                  root2.makeTree(self.funDefinitions(root2))

                else:
                  error_free=0
                  print("error, expected sali at line", self.current_token.token_line)
              else:
                error_free=0
                print("error, expected bda at line", self.current_token.token_line)
            else:
              error_free=0
              print("error, expected a closing parenthese at line", self.current_token.token_line)
          else:
            error_free=0
            print("error, expected an opening parenthese at line", self.current_token.token_line)
        else:
          error_free=0
          print("error, expected an identifier at line", self.current_token.token_line)
      #the second case here, is when the function has no output so the identifier (name of the function) comes directly after 'Dalla'
      elif(self.current_token.token_num == tokensDict["ID"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        if(self.current_token.token_num == tokensDict["("]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          root.makeTree(self.parameters())
          if(self.current_token.token_num == tokensDict[")"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            if(self.current_token.token_num == tokensDict["bda"]):
              root.makeTree(self.current_token)
              self.current_token = next(self.tokensList_cycle)
              root.makeTree(self.statements())
              if(self.current_token.token_num == tokensDict["sali"]):
                root.makeTree(self.current_token)
                self.current_token = next(self.tokensList_cycle)
      else:
        error_free=0
        print("expected an ID or 'dalla' at line", self.current_token.token_line)
    else:
      return None
      
    return root
# acceptor of parameters 
  def parameters(self):
    global funct_parameters
    root = Node ("PARAMS")
    #parameters of a function, in function definitions start with the type of the variables
    while((self.current_token.token_num == tokensDict["aadad"] or self.current_token.token_num == tokensDict["ramz"]) and self.current_token.token_num != tokensDict[")"]):
      root.makeTree(self.current_token)
      funct_parameters.append(self.current_token.token_name)
      self.current_token = next(self.tokensList_cycle)
      #after a type we should have an identifier
      if(self.current_token.token_num== tokensDict["ID"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        # parameters are separated with commas
        if(self.current_token.token_num== tokensDict[","]):
          root.makeTree(self.current_token)
          self.current_token= next(self.tokensList_cycle)
    return root

  #acceptor of statements  
  def statements(self):
    root = Node("STATS")
    #if a statements starts with '(' o an ID or a literal or 'tebaa' or 'qra', means it is either an assignment of a fucntion call
    if(self.current_token.token_num == tokensDict["("] or self.current_token.token_num == tokensDict["ID"] or self.current_token.token_num == tokensDict["LIT"] or self.current_token.token_num == tokensDict["tebaa"] or self.current_token.token_num == tokensDict["qra"]):
        root.makeTree(self.asgOrFnctCall())
        #after the assignment of the function call we call statements() recursively      
        root.makeTree(self.statements())
    # if the statement starts with 'ila', it means that it is a selection statemnt 
    elif(self.current_token.token_num == tokensDict["ila"]):
      root.makeTree(self.selectionStmt())
      root.makeTree(self.statements())
    # if the statement starts with 'mahed', it means it is a repititionstatement
    elif(self.current_token.token_num == tokensDict["mahed"]):
      root.makeTree(self.repetitionStmt())
      root.makeTree(self.statements())
    #if the statement starts wih 'hbess', it means it is a break statemnt 
    elif(self.current_token.token_num == tokensDict["hbess"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.statements())
    # if the statement starts with 'rejaa',it is a return-statement
    elif(self.current_token.token_num == tokensDict["rejaa"]):
      root.makeTree(self.returnStmt())
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.statements())
    # finally, if it starts with a type, it is a variable declaration
    elif (self.current_token.token_num == tokensDict["aadad"] or self.current_token.token_num == tokensDict["ramz"] or self.current_token.token_num == tokensDict["&"]):
      root.makeTree(self.varDeclarations())
      root.makeTree(self.statements())
    else:
      return None
      
    return root
#  acceptor for the assignment of function call
  def asgOrFnctCall(self):
    global current_ID
    global curr_type
    root = Node("ASGORFCT")
    if(self.current_token.token_num == tokensDict["ID"]):
      # check whether the identifier is defined
       if(self.current_token.token_name in self.symbolTable):
        curr_type=self.symbolTable[self.current_token.token_name]
        root.makeTree(self.current_token)
        current_ID=self.current_token.token_name
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.temp4())
       else:
        root.makeTree(self.current_token)
        current_ID=self.current_token.token_name
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.temp4())
         
    elif(self.current_token.token_num == tokensDict["qra"]):
      root.makeTree(self.qra())    
    elif(self.current_token.token_num == tokensDict["tebaa"]):
      root.makeTree(self.tebaa())
    elif(self.current_token.token_num == tokensDict["("]):
      root.makeTree(self.expression())
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.asgOp()) 
    elif(self.current_token.token_num == tokensDict["LIT"]):
      # if the assignment starts with a literal , we should keep track of its type, for type checking 
      if(re.match("[0-9]",self.current_token.token_name)):
        curr_type="aadad"
      else:
        curr_type="ramz"
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.asgOp())
    return root
      
  # acceptor  for asgOp, that is called inside an assignment statement 
  def asgOp(self):
    global error_free
    root = Node("ASGOP")
    # after the firs ID/ LIT we may have an operator+ expression
    if(self.current_token.token_num == tokensDict["+"] or self.current_token.token_num == tokensDict["-"] or self.current_token.token_num == tokensDict["/"] or self.current_token.token_num == tokensDict["*"] or self.current_token.token_num == tokensDict["%"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.expression())
      self.current_token = next(self.tokensList_cycle)
    # the second case is having directly the assignment symbol '=>'
    if(self.current_token.token_num == tokensDict["=>"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num == tokensDict["ID"]): 
        if(self.current_token.token_name in self.symbolTable):
          if(curr_type==self.symbolTable[self.current_token.token_name]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          else:
            error_free=0
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            print("wrong assignment types at line",self.current_token.token_line)
        else:
          error_free=0
          print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)

        if(self.current_token.token_num == tokensDict[";"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
        else:
          error_free=0
          print("error, expected ; at line",self.current_token.token_line)
      else:
        error_free=0
        print("error, expected an ID at line", self.current_token.token_line)
    else:
      error_free=0
      print("error, expected '=>' at line", self.current_token.token_line) 
    return root
 # acceptor for fctcall
  def fctCall(self):
    global error_free
    root = Node("FCTCALL")
    if(self.current_token.token_num == tokensDict["ID"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.IDs())
        self.current_token = next(self.tokensList_cycle)
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          root.makeTree(self.OutpStore())
        else:
          error_free=0
          print("expected a closing parenthese at line", self.current_token.token_line)
      else:
        error_free=0
        print("expected an opening parenthese at line", self.current_token.token_line)
    elif(self.current_token.token_num == tokensDict["qra"]):
      root.makeTree(self.qra())
    elif(self.current_token.token_num==tokensDict["tebaa"]):
      root.makeTree(self.tebaa())
    return root
# acceptor for IDs, which represent the IDs passed as arguments in a function call
  def IDs(self):
    global error_free
    global outp
    global qraOrtebaa
    root = Node("IDS")
    var=next(parametersCy)
    if(var=="Output"):
      outp=next(parametersCy)
      var=next(parametersCy)
   # IDs starts with an ID then if it is followed with ',' it calls (IDs) recursivly 
    if(self.current_token.token_num == tokensDict["ID"]):
      if(self.current_token.token_name in self.symbolTable):
        if(self.symbolTable[self.current_token.token_name]==var or qraOrtebaa==1):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          if(self.current_token.token_num == tokensDict[","]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            root.makeTree(self.IDs())
        else:
          error_free=0
          print("wrong parameter type for at line",self.current_token.token_line, "expected",var,"found",self.symbolTable[self.current_token.token_name])
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
      else:
        error_free=0
        print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
     
    return root

#acceptor for OutpStore, which refers the second part of the function call where we may  store the returned value to a variable.
  def OutpStore(self):
    global outp
    global error_free
    root = Node("OUTP")
    if(self.current_token.token_num == tokensDict["=>"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num == tokensDict["ID"]):
        # check whether the ID is defined  before
        if(self.current_token.token_name in self.symbolTable):
          #cheks whether the type of the ID matches the expected type of the function
          if(self.symbolTable[self.current_token.token_name]!=outp):
              error_free=0
              print("wrong output type, should be",outp,"at line")
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          if(self.current_token.token_num==tokensDict[";"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          else:
            error_free=0
            print("error, expected a ; at line", self.current_token.token_line)
        else:
          error_free=0
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
      else:
        error_free=0
        print("error, expected an ID", self.current_token.token_num)
    #  checks whether the function call is terminated by a semicolen
    elif(self.current_token==tokensDict[";"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
    else:
      error_free=0
      print("error, expected a ; at line", self.current_token.token_line)
    return root

  # acceptor of a qra function (<=>scanf)        
  def qra(self):
    global qraOrtebaa
    root = Node ("QRA")
    qraOrtebaa=1
    #qra function should start withe the reserved word 'qra'
    if(self.current_token.token_num == tokensDict["qra"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      # the word 'qra' should be followed by parenthe (
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.IDs())
        # after IDs, the parenthesis should be closed, and the statement should end with a semicolen
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          if(self.current_token.token_num == tokensDict[";"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          else:
              error_free=0
              print("error, expected a ; at line", self.current_token.token_line)
        else:
          error_free=0
          print("error, expected a ) at line", self.current_token.token_line)
      else:
        error=0
        print("error, expected a ( at line", self.current_token.token_line)
    qraOrtebaa=0
    return root
  
  #acceptor for a tebaa function (<=>print)
  def tebaa(self):
    global error_free
    global qraOrtebaa
    qraOrtebaa=1
    root = Node("TEBAA")
    # tebaa function should start with the reserved word 'tebaa' 
    if(self.current_token.token_num == tokensDict["tebaa"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      # after the word tebaa, we should have a parenthese (
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.combination())
        # after combinations between parenthesis we should have the closing parenthese, and end the statement with a semicolen
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          if(self.current_token.token_num == tokensDict[";"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)  
          else:
              error_free=0
              print("error, expected a ; at line", self.current_token.token_line)
        else:
          error_free=0
          print("error, expected a ) at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected a ( at line", self.current_token.token_line )
    qraOrtebaa=0
    return root

  #acceptor of temp4 which gets called after an identifier to identify whether it's a variable name (assignment) or a function name (function call)
  def temp4(self):
    global current_ID
    global current_function
    global parametersCy
    global curr_type
    global error_free
    root = Node("TEMP4")
    #case if it's a function call
    if(self.current_token.token_num == tokensDict["("]):
      root.makeTree(self.current_token)
      current_function=current_ID
      self.current_token = next(self.tokensList_cycle)
      var="smtg"
      while(var!=current_function):
        var=next(parametersCy)
      root.makeTree(self.IDs())
      if(self.current_token.token_num == tokensDict[")"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.OutpStore())
      else:
        error_free=0
        print("error, expected a ) at line", self.current_token.token_line)
    #case of an assignment
    elif(self.current_token.token_num == tokensDict["=>"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if (self.current_token.token_num == tokensDict["ID"]):
        if(self.current_token.token_name in self.symbolTable):
          if(curr_type==self.symbolTable[self.current_token.token_name]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          else:
            error_free=0
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            print("wrong assignment types at line",self.current_token.token_line)
        else:
          error_free=0
          print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)

        if(self.current_token.token_num == tokensDict[";"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
        else:
          error_free=0
          self.current_token = next(self.tokensList_cycle)
          print("error, expected ; at line ",self.current_token.token_num,self.current_token.token_line)
      else:
        error_free=0
        print("error, expected an identifier at line", self.current_token.token_line)
    #case of an assignment with an expression on the LHS
    elif(self.current_token.token_num == tokensDict["+"] or self.current_token.token_num == tokensDict["-"] or self.current_token.token_num == tokensDict["/"] or self.current_token.token_num == tokensDict["*"] or self.current_token.token_num == tokensDict["%"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.expression())
      if(self.current_token.token_num == tokensDict["=>"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        if (self.current_token.token_num == tokensDict["ID"]):
          if(self.current_token.token_name in self.symbolTable):
            if(self.symbolTable[self.current_token.token_name]!="aadad"):
               print("wrong assignment types at line",self.current_token.token_line)
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          else:
            error_free=0
            print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
          if(self.current_token.token_num == tokensDict[";"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
        else:
         error_free=0
         print("error, expected an identifier at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected a '=>' at line", self.current_token.token_line)

    return root

#acceptor for assignment statement
  def assignmentStmt(self):
    global error_free
    root = Node("ASSIGNMENT")
    #an acceptor expects an expression first  so the acceptor of expression is called
    root.makeTree(self.expression())
    # symbol "=>" is expected after the expression
    if(self.current_token.token_num == tokensDict["=>"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      # an Identifier is expected here to store the value
      if(self.current_token.token_num == tokensDict["ID"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        #at the end of the assignment statement a ; is expected 
        if(self.current_token.token_num== tokensDict[";"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
        else:
          error_free=0
          print("error, expected a ; at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected an identifier at line", self.current_token.token_line)
    else:
     error_free=0
     print("error, expected a '=>' at line", self.current_token.token_line)

    return root
# selection statement acceptor
  def selectionStmt(self):
    global error_free
    root = Node ("SELECT")
    #a selection statement should start with  'ila' 
    if(self.current_token.token_num == tokensDict["ila"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.condition())
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          #after the condition between parenthesis, ':' is expected 
          if(self.current_token.token_num== tokensDict[":"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            root.makeTree(self.statements())
            # ':' is expected at the end of the if-stmt as well
            if(self.current_token.token_num == tokensDict[":"]):
              root.makeTree(self.current_token)
              self.current_token = next(self.tokensList_cycle)
              # the statment 'ilaghalat' <=> else, is optional, so if it is not there it doesn't raise any error
              if(self.current_token.token_num == tokensDict["ilaghalat"]):
                root.makeTree(self.selectionTemp())

            else:
              error_free=0
              print("error, expected a : at line", self.current_token.token_line)
          else:
             error_free=0
             print("error, expected a : at line", self.current_token.token_line)
        else:
          error_free=0
          print("error, expected a ) at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected a ( at line", self.current_token.token_line)
    return root

#acceptor for selectionTemp ( called after 'else' is encountered)
  def selectionTemp(self):
    global error_free
    root = Node("SELECTEMP")
    #double checks that the else-statement starts with 'ilaghalate' 
    if(self.current_token.token_num == tokensDict["ilaghalat"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      #checks that ilaghalate is followed by :
      if(self.current_token.token_num == tokensDict[":"]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.statements())
        # checks that ilaghalate ends with :
        if(self.current_token.token_num == tokensDict[":"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
 
        else:
          error_free=0
          print("error, expected a : at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected a : at line", self.current_token.token_line)

    return root

#acceptor of repetition statements (loops)
  def repetitionStmt(self):
    global error_free
    root = Node("REPERT")
    #  a loop starts with reserved word 'mahed'
    if(self.current_token.token_num == tokensDict["mahed"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num == tokensDict["("]):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.condition())
         #mahed should be followed by a condition between parenthesis
        if(self.current_token.token_num == tokensDict[")"]):
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
          #a semicolen is expected after parenthesis
          if(self.current_token.token_num == tokensDict[":"]):
            root.makeTree(self.current_token)
            self.current_token = next(self.tokensList_cycle)
            root.makeTree(self.statements())
            #a semicolen is expected also at the end of the loop
            if(self.current_token.token_num == tokensDict[":"]):
              root.makeTree(self.current_token)
              self.current_token = next(self.tokensList_cycle)
          else:
            error_free=0
            print("error, expected a : at line", self.current_token.token_line)
        else:
          error_free=0
          print("error, expected a ) at line", self.current_token.token_line)
      else:
        error_free=0
        print("error, expected a ( at line", self.current_token.token_line)

    return root

  # acceptor for a return-statement     
  def returnStmt(self):
    root = Node("RETURN")
    # a return statement should start with the reserved word "rejaa"
    if(self.current_token.token_num == tokensDict["rejaa"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.returnedVal())

    return root
  # acceptor for  a returned value
  def returnedVal(self):
    global error_free
    root = Node("RETURNEDVAL")
    # a returned value should be either an identifier or a literal 
    if(self.current_token.token_num == tokensDict["ID"] or self.current_token.token_num == tokensDict["LIT"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      if(self.current_token.token_num != tokensDict[";"]):
        error_free=0
        print("expected a ; after return statement")
      root.makeTree(self.current_token)
    return root

  #  acceptor for expression
  def expression(self):
    global error_free
    root = Node("EXP")
    # an expression may start with parenthesis
    if(self.current_token.token_num == tokensDict["("]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.expression())
      if(self.current_token.token_num == tokensDict[")"]):
        root.makeTree(self.current_token)
        root.makeTree(self.expTemp(root))
      else:
        error_free=0
        print("error, expected a ) at line", self.current_token.token_line)
    else:
      # an expresssion may also start with an operand dirctly
      root.makeTree(self.operand())
      root.makeTree(self.expTemp())

    return root
  # acceptor of exptemp which is called after an operand
  def expTemp(self):
    root = Node("EXPTEMP")
    # and exptemp should start with an operator
    if(self.current_token.token_num == tokensDict["+"] or self.current_token.token_num == tokensDict["-"] or self.current_token.token_num == tokensDict["/"] or self.current_token.token_num == tokensDict["*"] or self.current_token.token_num == tokensDict["%"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      # after the operator we should have an expression
      root.makeTree(self.expression())
    else:
      return None

    return root
 
#  acceptor of operand
  def operand(self):
    global cond
    global error_free
    global cond_type
    root = Node("OPERAND")
    #and operand is either a literal or identifier
    if(self.current_token.token_num == tokensDict["LIT"] or self.current_token.token_num == tokensDict["ID"] ):
      # if the operand is an identifier it should be defined already in the symbol table
      if(self.current_token.token_name in self.symbolTable or self.current_token.token_num == tokensDict["LIT"] ):
        #the operands should be of type 'aadad', because we don't allow operations on characters unless it is inside a condition
        if((self.current_token.token_num == tokensDict["LIT"] and re.match("[0-9]",self.current_token.token_name)) or (self.current_token.token_num == tokensDict["ID"] and self.symbolTable[self.current_token.token_name]=="aadad") or cond!=0):
          if(cond==1):
            # if the operand is inside a condition we should keep track of the type of the type of the first operand
            if((self.current_token.token_num == tokensDict["LIT"] and re.match("[0-9]",self.current_token.token_name)) or (self.current_token.token_num == tokensDict["ID"] and self.symbolTable[self.current_token.token_name]=="aadad") ):
              cond_type="aadad"
            else:
              cond_type="ramz"
          elif(cond==2):
            # if the operand is inside a condition and it comes after the comparison operators we should compare its type with the first one to make sure we are comparing to operands of the same type
            if(not ((self.current_token.token_num == tokensDict["LIT"] and re.match("[0-9]",self.current_token.token_name)) or (self.current_token.token_num == tokensDict["ID"] and self.symbolTable[self.current_token.token_name]=="aadad")) and cond_type=="aadad"):
              error_free=0
              print("incomparable types inside condition at line",self.current_token.token_line )
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
        else:
          error_free=0
          print("invalid type at line ",self.current_token.token_line,self.current_token.token_name)
          root.makeTree(self.current_token)
          self.current_token = next(self.tokensList_cycle)
      else:
        error_free=0
        print("undefined identifier",self.current_token.token_name,"at line",self.current_token.token_line)
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
      
    else:
      error_free=0
      print("error,expected  an identifier or literal at line", self.current_token.token_line)
      return None
    
    return root
# acceptor of conditions
  def condition(self):
    global cond
    global error_free
    root = Node("CONDITION")
    #case where a condition may start with machi
    if(self.current_token.token_num == tokensDict["MACHI"]):
      self.current_token = next(self.tokensList_cycle)
    cond=1
    root.makeTree(self.operand())
    root.makeTree(self.compEx())
    cond=2
    root.makeTree(self.operand())
    cond=0
    root.makeTree(self.conditionTemp())
   
    return root
#acceptor for combination
  def combination(self):
    root = Node("COMBINATION")
    if(self.current_token.token_num == tokensDict["LIT"]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
      root.makeTree(self.combination())
    elif(self.current_token.token_num == tokensDict["ID"]):
      #check if the ID is defined before
      if(self.current_token.token_name in self.symbolTable):
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.combination())
      else:
        error_free=0
        print("undefined identifier: ",self.current_token.token_name,"at line",self.current_token.token_line)
        root.makeTree(self.current_token)
        self.current_token = next(self.tokensList_cycle)
        root.makeTree(self.combination())
    else:
      return None

    return root

 #acceptor of comparison expressions, it gets called after finding an identifier or a literal inside a condition
  def compEx(self):
    global error_free
    root = Node("COMPEX")
    if(self.current_token.token_num == tokensDict["<"] or self.current_token.token_num == tokensDict[">"] or self.current_token.token_num == tokensDict["<"] or self.current_token.token_num == tokensDict["<="] or self.current_token.token_num == tokensDict[">="] or self.current_token.token_num == tokensDict["="] or self.current_token.token_num == tokensDict["!="]):
      root.makeTree(self.current_token)
      self.current_token = next(self.tokensList_cycle)
    else:
      error_free=0
      print("error, expected a comparision operator", self.current_token.token_num)
    return root

#acceptor of conditionTemp which handles logical operators in conditions (example x<0 WLA y>12)
  def conditionTemp(self):
    root = Node("CONDITIONTEMP")
    if(self.current_token.token_num == tokensDict["WLA"] or self.current_token.token_num == tokensDict["O"]):
      root.makeTree(self.logEx())
      root.makeTree(self.condition())
    else:
      return None
    return root

  #acceptor of logex
  def logEx(self):
    root = Node("LOGEX")
    #we check if the current token is one of the logical operators, so that we append it to the parse tree
    if(self.current_token.token_num == tokensDict["WLA"] or self.current_token.token_num == tokensDict["O"]):
      root.makeTree(self.current_token)
      self.current_token= next(self.tokensList_cycle)
    return root