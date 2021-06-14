/****************************************************
*****************************************************
            Assembly to Machine Language
                  ASSEMBLER CODE
******************************************************
******************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//defining the structure hashtable, which will contain a key (operand) and a value (address)
typedef struct {
  char key[5];
  char value[5];
} hashtable;

int HASHSIZE = 100; //size of hashtables used
int line=0; //keeps track of the line numbers in the code, to later use them for addressing purposes
hashtable* symbolTable;  //hashtable used to keep track of symbols used in the program
hashtable* labelTable; //hashtable used to keep track of labels in the program
FILE* code_with_spaces; //file used to print the machine codes with spaces between opcode and operands
int insertElement (hashtable*, char*, char*); //function used to insert an element in a particular hashtable
int find (char*, hashtable*); //function used to retrieve a value from a particular hashtable
void initializeData (FILE* , FILE*); //function used to handle the data part
void initializeInput (FILE*, FILE*); //function used to handle the input part of the program
void initializeProgram (FILE*, FILE*); //function used to handle the code part of the program
int hashfunction (char* key); //hash function which generates a hash code for each key
void initializeTables (); //function used to allocate memory for the hashtables used in our program
void initializeLabels();

int main(void) {

  //file where the assembly code is stored
  FILE* inputfile;
  //file where the machine code will be stored
  FILE* outputfile;
  initializeTables();
  inputfile = fopen("ALoutput.txt", "r");
  outputfile = fopen("machinecode.txt", "w");
  code_with_spaces = fopen("MachineCodeWithSpaces.txt", "w");


  if(inputfile==NULL) {
    printf("File not found!\n");
  }

  else {
    initializeLabels();
    initializeData(inputfile, outputfile);
    initializeProgram(inputfile, outputfile);
    initializeInput(inputfile, outputfile);
    fclose(outputfile);
    fclose(code_with_spaces);
  }

}

void initializeTables () {

  //allocating space for the symbol table
  symbolTable = calloc(HASHSIZE, sizeof(hashtable));

  //allocating space for the label table
  labelTable = calloc (HASHSIZE, sizeof(hashtable));

  //initializing all rows of the table to hold the empty string
  for (int i=0; i<HASHSIZE; i++) {
    labelTable[i].key[0] = '\0';
    labelTable[i].value[0] = '\0';
    symbolTable[i].key[0] = '\0';
    symbolTable[i].value[0] = '\0';
  }
}

void initializeData (FILE* inputfile, FILE* outputfile){
  fseek(inputfile, 0,0);
  char opcode[10], op1[10], op2[10], value[10];
  int x;
  strcpy(opcode, "\0");

  fscanf(inputfile, "%s%s%s", opcode, op1, op2);

  while(strncmp(opcode, "+99",3)!=0) {
      
    opcode[strlen(opcode)]= '\0';

    if(strcmp(opcode, "DEF")!=0) {
      printf("Invalid opcode at line %d! Assembly failed!\n", line);
      
      return;
    }
    

     sprintf(value, "%0*d", 4, line);
     line++;

     // inserting the symbol into hashtable
    int x = insertElement(symbolTable, op1, value);
    //int y= findSymbol(op1, symbolTable);
    int d = hashfunction(op1);

    if(x==2) {
      printf("Symbol %s couldn't be inserted!\n", op1);
      return;
    }
    
    // ****************************************

    fprintf(outputfile, "+0%s%s\n", value, op2);
    fprintf(code_with_spaces, "+0 %s %s\n", value, op2);


    fscanf(inputfile, "%s%s%s", opcode, op1, op2);
  }

  //end of the loop, meaning a separator was found
  // print the separator to the machine code File

  fprintf(outputfile, "%s%s%s\n", opcode, op1, op2);
  fprintf(code_with_spaces, "%s %s %s\n", opcode, op1, op2);

}

void initializeProgram (FILE* inputfile, FILE* outputfile) {

  //variables used to scan the assembly code instructions
  char opcode[10], op1[10], op2[10];
  //variable that holds the machine code version of the opcode
  char value[10];
  //temporary variables for formatting reasons
  char opcode2[10], temp[10];
  //three variables used to hold hash codes 
  int h1, h2, h3; 
  opcode2[0]='\0';
  opcode[0]='\0';
  

  //looping until a separator is found
  while(strncmp(opcode, "+99", 3)!=0) {
    //incrementing the line number as we loop over the lines in the fine
    line++;
    //scanning line by line
    fscanf(inputfile, "%s %s %s", opcode, op1, op2);
    opcode[strlen(opcode)]='\0';

    //first case: if the instruction is a label assignment
    if(strcmp(opcode, "ASG")==0) {
      strcpy(value, "+8");
      opcode2[0]='\0';
      
      //filling the temporary variable with the address in the format 000X for better readability 
      sprintf(temp, "%0*d", 4, line+2);

      /*//inserting the label into the label table
      insertElement(labelTable, op1, temp);
      strcpy(op1, labelTable[hashfunction(op1)].value);*/
      strcpy(op1, labelTable[hashfunction(op1)].value);
    }
    
  else {
    //looking up the first opcode in the symbol table
    h1 = find(op1, symbolTable);

    //looking up the second opcode in the label table
    h2 = find(op2, labelTable);

    //looking up the second opcode in the symbol table
    h3 = find(op2, symbolTable);

    /*First operand is an immediate value, 
    second operand is an immediate value as well*/
    if (h1==-999 && h2==-999 && h3==-999) {
      opcode2[0] = '0';
    }
    
    /*First operand is an immediate value
    second operand is either a label or a symbol*/
    else if ((h1==-999 && h3!=-999) ||
    (h1==-999 && h2!=-999)){
      opcode2[0] = '2';
      //Swapping the second operand with its address
      if(h2!=-999) {
        //case where the second operand is a label, it gets swapped with its address
        strcpy(op2, labelTable[h2].value);
        printf("heeere!\n");
      }
      else {
        //case where the second operand is a symbol, it gets swapped with its address
        strcpy(op2, symbolTable[h3].value);
      }
    }

    
    /*First operand is a symbol, 
    second operand is either a label or a symbol*/
    else if ((h1!=-999 && h3!=-999) ||
    (h1!=-999 && h2!=-999)){
      opcode2[0] = '1';
      //swapping the first operand with its address
      strcpy(op1, symbolTable[h1].value);
      
      if(h2!=-999) {
        //case where the second operand is a label, it gets swapped with its address
        strcpy(op2, labelTable[h2].value);
      }
      else {
        //case where the second operand is a symbol, it gets swapped with its address
        strcpy(op2, symbolTable[h3].value);

      }
    }

    /*First operand is an symbol,

    second operand is an immediate value*/
    else if ((h1!=-999 && h3==-999 && h2==-999)){
      opcode2[0] = '3';

      //swapping the first operand with its address
      strcpy(op1, symbolTable[h1].value);
    }

    //*********************************************
    //if else statements to replace the opcodes with their machine language equivalents

    if(strcmp(opcode, "MOV")==0) {
    strcpy(value,"+0");
    
    }
    else if(strcmp(opcode, "ADD")==0){
        strcpy(value,"+1");
    }
    else if(strcmp(opcode, "SUB")==0){
      strcpy(value,"-1");
    }
    else if(strcmp(opcode, "MUL")==0){
      strcpy(value,"+2");
    }
    else if(strcmp(opcode, "DIV")==0){
      strcpy(value,"-2");
    }
    else if(strcmp(opcode, "SQR")==0){
      strcpy(value,"+3");
    }
    else if(strcmp(opcode, "SQRT")==0){
      strcpy(value,"-3");
    }
    else if(strcmp(opcode, "EQU")==0){
      strcpy(value,"+4");
    }
    else if(strcmp(opcode, "NEQU")==0){
      strcpy(value,"-4");
    }
    else if(strcmp(opcode, "GTE")==0){
      strcpy(value,"+5");
    }
    else if(strcmp(opcode, "SLT")==0){
      strcpy(value,"-5");
    }
    else if(strcmp(opcode, "ATA")==0){
    strcpy(value,"+6");
    }
    else if(strcmp(opcode, "CFA")==0){
      strcpy(value,"-6");
    }
    else if(strcmp(opcode, "READ")==0){
      strcpy(value,"+7");
    }
    else if(strcmp(opcode, "PRNT")==0){
      strcpy(value,"-7");
    }
    else if(strcmp(opcode, "HALT")==0){
      strcpy(value,"+9");
    }
    else if(strncmp(opcode, "+99",3)==0) {
      // case where a separator is found
      //print the separator to the file and break
      fprintf(outputfile, "%s%s%s\n", opcode, op1, op2);
      fprintf(code_with_spaces, "%s %s %s\n", opcode, op1, op2);
      break;
    }
    else {
      printf("Invalid opcode %s at line %d\n",opcode,++line);
    
      break;
    }
 //}
  //************************************************
  strcat(value, opcode2);
  //print the machine code instruction to the output file, and print it with spaces in the other file
  fprintf(outputfile, "%s%s%s\n", value, op1, op2);
  fprintf(code_with_spaces, "%s %s %s\n", value, op1, op2);

  }
  
}
}
int insertElement (hashtable *HT, char* key, char* value) {

  int h, flag=1, tries=0, i=1, i_n;

  h = hashfunction (key);
  i_n = h;
 
  //if the key isn't mapped to an already full cell, proceed to insertion
 if(HT[h].key[0]=='\0') {
    strcpy (HT[h].key, key);
    strcpy (HT[h].value, value);

    return 1;
  }

 else {
   //looping through the table until we find an empty cell whose index is the hash code that we generated
    while(HT[h].key[0]!='\0') {
      //handling collisions 
      h =((h+(i*i))%HASHSIZE);
      i++;
      tries++;
      //if we kept generating the hash codes and we exceeded the table size
      if(tries>HASHSIZE) {
        flag=0;
        break;
      }
    }
}

  if(flag) {
  //if a hashing index could be found
    strcpy (HT[h].key, key);
    strcpy (HT[h].value, value);
    
    return 1;
  }
  else
    //if no hashing index could be found
    return 2;
}

int hashfunction (char* key) {

  int hashed;
  int t;

  //hashing function that generates a hash code for each key
  for (hashed=0; *key!='\0'; key++) {
    hashed = *key + 28*hashed;
  }

  return hashed % HASHSIZE;
}

int find (char* key, hashtable* HT) {
  int h, i_n,i=1, tries=0;

  // get the hash value depending on the key
  h = hashfunction(key);

  //storing the hash code generated by the function in another
  //temporary variable
  i_n = h;
  

  //iterating over the table until we find a cell whose key matches our symbol
  while(HT[h].key[0]!='\0' && tries<=HASHSIZE) {
    if(strcmp(HT[h].key, key)==0) {

      //return the hash code if the key is found
      return h;
    }
    // if the symbol is not found, alter the hash code according to how we handled
    //the collisions
    else {
      h=((h+(i*i))%HASHSIZE);
      i++;
    }
    tries++;
  }
  //if we exit the loop without finding the key in the table, return an arbitrary negative value
  return -999;
}

  void initializeInput(FILE* inputfile,FILE* outputfile){
  char opcode[10], op1[10], op2[10];
 while (!feof(inputfile)){
      fscanf(inputfile, "%s %s %s\n", opcode, op1, op2);
      fprintf(outputfile, "%s%s%s\n", opcode, op1, op2);
      fprintf(code_with_spaces, "%s %s %s\n", opcode, op1, op2);
      }
  }



void initializeLabels(void){
  FILE* fptr;
  char opcode[10], op1[10], op2[10],temp[10];
  int line2=0, cnt=0;
  fptr= fopen("ALoutput.txt", "r");
 if(fptr==NULL) {
    printf("File not found!\n");
  }

  while(!feof(fptr)){
      fscanf(fptr, "%s %s %s", opcode, op1, op2);
      if(!strcmp(opcode,"+99")){
        //we start counting lines after the first seperator to get the line number in the program part 
        line2=-1;
      }
      if(strcmp(opcode, "ASG")==0) {
      //filling the temporary variable with the address in the format 000X for better readability
      sprintf(temp, "%0*d", 4, line2-cnt); 
      //inserting the label into the label table
      insertElement(labelTable, op1, temp);
      // cnt counts the number of occurences of ASG instruction to keep track of the number of lines removed in the machine code translation
     cnt++;
    }
            line2++;

  }
  fclose(fptr);
}