/****************************************************
*****************************************************
            Machine Language Interpretation
                  INTERPRETER CODE
******************************************************
******************************************************/

#include <stdio.h>
#include<stdlib.h>
#include <string.h>
#include<math.h>

//dataMemory is an array of long long integers that holds the data needed for the program to run
long long int dataMemory[10000];
//programMemory is an array of strings where the program part of the code gets loaded
char programMemory[10000][12];

void loadData(FILE *);
int loadProgram(FILE *);

int main(void){
  FILE *infp;
  char opcodestr[3],op1s[5],op2s[5];
  int IP=0, ACC=0, opcode, flag, op1, op2, X;
  long long int instruction, value;

  infp = fopen("machinecode.txt","r");
  
  loadData(infp);
  X=loadProgram(infp);

  while(IP < X){
    //following is the process of parsing each part of the instruction to an integer 
    strncpy(opcodestr,programMemory[IP],2);
    flag = programMemory[IP][2]-'0';
    //Copying the first operand to another string and converting it to an integer 
    op1s[0] = programMemory[IP][3];
    op1s[1] = programMemory[IP][4];
    op1s[2] = programMemory[IP][5];
    op1s[3] = programMemory[IP][6];
    op1s[4] = '\0';
    //Copying the second operand to another string and converting it to an integer 
    op2s[0] = programMemory[IP][7];
    op2s[1] = programMemory[IP][8];
    op2s[2] = programMemory[IP][9];
    op2s[3] = programMemory[IP][10];
    op2s[4] = '\0';
    op1=atoi(op1s);
    op2=atoi(op2s);
    opcode=atoi(opcodestr);
    IP++;

    switch(opcode){
      case +0:
        if(flag == 0){
          //initialize the content of the accumulator to the value of op1
          ACC = op1;
        }
        else if(flag == 3){
          //initialize the content of the accumulator to the value of memory location op1
          ACC = dataMemory[op1];
        }
        if(flag == 1){
          //initialize the content of memory location op2 to the value of memory location op1
          dataMemory[op2] = dataMemory[op1];
        }
        else if(flag == 2){
          //initialize the content of memory location to the value of the accumulator
          dataMemory[op2] = ACC;
        }
        break;
      case +1:
        if(flag == 1){
          //add the content of memory location op1 to the value of the accumulator and store the result in the memory location op2 
          dataMemory[op2] = dataMemory[op1] + ACC;
        } 
        else if(flag == 2){
          //add the value of op1 to the value of the accumulator and store the result in the memory location op2 
          dataMemory[op2] = op1 + ACC;
        }
        break;
      case -1:
        if(flag == 1){
          //subtract the content of memory location op1 from the value of the accumulator and store the result in the memory location op2
          dataMemory[op2] = dataMemory[op1] - ACC;
        }
        else if(flag == 2){
          //subtract the value of op1 from the value of the accumulator and store the result in the memory location op2 
          dataMemory[op2] = op1 - ACC;
        }
        break;
      case +2:
        if(flag == 1){
          //multiply the content of memory location op1 by the value of the accumulator and store the result in the memory location op2
          dataMemory[op2] = dataMemory[op1] * ACC;
        }
        else if(flag == 2){
          //multiply the value of op1 by the value of the accumulator and store the result in the memory location op2 
          dataMemory[op2] = op1 * ACC;
        }
        break;
      case -2:
        if(flag == 1){
          //divide the content of memory location op1 by the value of the accumulator and store the result in the memory location op2
          if(ACC != 0){
            dataMemory[op2] = (long long int) dataMemory[op1] / ACC;
          }
          else{
            printf("ERROR!CANNOT divide by zerro");
            fclose(infp);
          }
        }
        else if(flag == 2){
          //divde the value of op1 by the value of the accumulator and store the result in the memory location op2 
          if(ACC != 0){
            dataMemory[op2] = (long long int) op1 / ACC;
          }
          else{
            printf("ERROR!CANNOT divide by zerro");
            fclose(infp);
          }
        }
        break;
      case +3:
        if(flag == 1){
          //square the content of memory location op1 and store the result in memory location op2
          dataMemory[op2] = dataMemory[op1] * dataMemory[op1];
        }
        else if(flag == 2){
          //square the value of op1 and store the result in mmeory location op2
          dataMemory[op2] = op1 * op1;
        }
        break;
      case -3:
        if(flag == 1){
          //square root the content of memory location op1 and store the result in memory location op2
          dataMemory[op2] = (long long int) sqrt((double) dataMemory[op1]);
        }
        else if(flag == 2){
          //square root the value of op1 and store the result in memory location op2
          dataMemory[op2] = (long long int) sqrt((double) op1);
        }
      case +4:
        if(flag == 1){
          //checks if the content of memory location op1 is equal to the value of accumulator, if so it jumps to memory location op2
          if(ACC == dataMemory[op1]){
            IP = op2;
          }
        }
        else if(flag == 2){
          //checks if the value of op1 is equal to the value of accumulator, if so it jumps to memory location op2
          if(ACC == op1){
            IP = op2;
          }
        }
        break;
      case -4:
        if(flag == 1){
          //checks if the content of memory location op1 is not equal to the value of accumulator, if so it jumps to memory location op2
          if(ACC != dataMemory[op1]){
            IP = op2;
          }
        }
        else if(flag == 2){
          //checks if the value of op1 is not equal to the value of accumulator, if so it jumps to memory location op2
          if(ACC != op1){
           
            IP = op2;
          }
        }
        break;
      case +5:
        if(flag == 1){
          //checks if the content of memory location op1 is greater than or equal to the value of accumulator, if so it jumps to memory location op2
          if(dataMemory[op1] >= ACC){
            IP = op2;
          }
        }
        else if(flag == 2){
          //checks if the value of op1 is greater than or equal to the value of accumulator, if so it jumps to memory location op2
          if(op1 >= ACC){
            IP = op2;
          }
        }
        break;
      case -5:
        if(flag == 1){
          //checks if the content of memory location op1 is less than the value of accumulator, if so it jumps to memory location op2
          if(dataMemory[op1] < ACC){
            IP = op2;
          }
        }
        else if(flag == 2){
          //checks if the value of op1 is less than the value of accumulator, if so it jumps to memory location op2
          if(op1 < ACC){
            IP = op2;
          }
        }
        break;
      case +6:
        //assign to array, adds the index (op1) to the start of the array address (memory location op2) and stores the value of the accumulator in the address calculated 
        if (flag==2)
        dataMemory[op1 + op2] = ACC;
        break;
      case -6:
        //copy from array, copies the content of memory location computed by adding the index to the array address and stores it in the accumulator
        ACC = dataMemory[op1+op2];
        break;
      case +7:
        //Read, gets input from the input part of the code and stores it in address OP1
        fscanf(infp, "%lld",&value);
        dataMemory[op1] = value;
        printf("value read is %lld\n",dataMemory[op1]);
        break;
      case -7:
        //print, gets value from memory location op1/ or an immediate value and prints it  to the screen
        if(flag==0){
          printf("%d",op1);
        }
        else if (flag==3){
          printf("%lld\n",dataMemory[op1]);
        }
        break;
      case +9:
        fclose(infp);
        break;
    }
  }
}

void loadData(FILE *infp){
  //this function takes as input the file pointer with the cursor pointing to the start of the data part of the code and load all the data (untill reaching a seperator)to the data memory
  long long int initialization;
  int index;
  fscanf(infp, "%lld", &initialization);
  while(initialization != 9999999999){
      dataMemory[index] = initialization % 10000;
      index++;
      fscanf(infp, "%lld\n", &initialization);
    }
}

int loadProgram(FILE *infp){
  //this function takes as input the file pointer with the cursor pointing to the start of the program part of the code and loads all the program (until reaching a seperator)to the program memory 

  int index = 0;
  char instruction[12];
  fscanf(infp, "%s\n", instruction);
  while(strcmp(instruction,"+9999999999") ){
    strcpy(programMemory[index],instruction);
    index++;
    fscanf(infp, "%s\n", instruction);
  }
  return index;
} 