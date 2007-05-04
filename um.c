#include <stdlib.h>
#include <stdio.h>

typedef unsigned platter;

/* allocates a buffer containing the program */
platter* read_prog(char *filename)
{
   platter *buf;
   FILE *f;
   int size;

   f=fopen(filename,"r");
   if (f==NULL) {
       fprintf (stderr,"failed to open file\n");
       exit (EXIT_FAILURE);
   }

   fseek(f,0,SEEK_END);
   size=ftell(f);
   buf=malloc(size);
   
   if (fread(buf,size,1,f) != 1) {
       fprintf (stderr,"failed to read file\n");
       exit (EXIT_FAILURE);
   }

   return buf;
}    

int main(int argc,char *argv[])
{
    platter registers[8] = {0};
    platter ** arrays;
    
    if (argc != 2) {
        fprintf (stderr,"usage: %s filename\n",argv[0]);
        exit (EXIT_FAILURE);
    }

    arrays=calloc(sizeof (platter**), 1); /* just allocate space for '0' */

    arrays[0]=read_prog(argv[1]); /* allocate a buffer containing the program */

    



    
    free (arrays[0]);  /* free the array '0' */
    return EXIT_SUCCESS;
}    
