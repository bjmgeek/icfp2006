#include <stdlib.h>
#include <stdio.h>

typedef unsigned platter;

typedef enum {
    conditional_move,
    array_index,
    array_ammendment,
    addition,
    multiplication,
    division,
    not_and,
    halt,
    allocation,
    abandonment,
    output,
    input,
    load_program,
    orthography } opcode;

struct machine_state { 
    platter registers[8];
    platter ** arrays;
    platter * finger;
    platter operation;
    opcode op;
};
    

/* allocates a buffer containing the program */
platter* read_prog(char *filename)
{
   platter *buf;
   FILE *f;
   int size=0;

   f=fopen(filename,"r");
   if (f==NULL) {
       fprintf (stderr,"failed to open file\n");
       exit (EXIT_FAILURE);
   }

   fseek(f,0,SEEK_END);
   size=ftell(f); /* to see how big the file is */
   rewind(f); 

   buf=calloc(size,1);
   fread(buf,size,1,f);
   
   return buf;
}    

opcode decode_operation (platter op) 
{
    return op >> 28;
}

void machine_step (struct machine_state * mstate)
{
    fprintf(stderr,"got opcode '%d'\n",mstate -> op);

    mstate->op = halt;
}

int main(int argc,char *argv[])
{
    struct machine_state *m;
    
    if (argc != 2) {
        fprintf (stderr,"usage: %s filename\n",argv[0]);
        exit (EXIT_FAILURE);
    }

    m=malloc(sizeof (struct machine_state));

    m->arrays=calloc(sizeof (platter**), 1); /* just allocate space for '0' */

    m->arrays[0]=read_prog(argv[1]); /* allocate a buffer containing the program */

    m->finger=m->arrays[0];

    /* "spin cycle" */
    while ((m->op=decode_operation(m->operation))!=halt) {
        machine_step(m);
    }
    
    free (m->arrays[0]);  /* free the array '0' */
    free (m->arrays);     /* free the list of arrays */
    free (m);
    return EXIT_SUCCESS;
}    
