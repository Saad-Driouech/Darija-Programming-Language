from Lexer import *
import Token
from Parser import *
from ALGenerator import *
import sys


def main():
  #creating an instance of the lexer
  lexer = Lexer()
  #calling the lex function to generate the token stream
  lexer.lex()
  #redirecting stdout to the output file
  sys.stdout = sys.__stdout__
  #creating an instance of the parser and passing the token stream to it along with the symbol table
  parser = Parser(lexer.tokensList, lexer.symbolTableDict)
  #calling the parse function to begin parsing
  parser.parse()

  generator = ALGenerator(lexer.tokensList)
  generator.instantiate()
  generator.generateAssembly()

if __name__ == "__main__":
  main()