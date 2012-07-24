/* $Id: um.c,v 1.18 2012/06/27 21:18:42 bminton Exp $ */
/* Brian Minton, brian@minton.name */
/* ICFP programming contest 2006 */

/* Universal Machine emulator */
/* NOTE: This code may only work on 32-bit machines */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <assert.h>

#define ARRAY(x) ((array*)(x))

typedef unsigned platter;

typedef enum {
    OPCODE_conditional_move,
    OPCODE_array_index,
    OPCODE_array_amendment,
    OPCODE_addition,
    OPCODE_multiplication,
    OPCODE_division,
    OPCODE_not_and,
    OPCODE_halt,
    OPCODE_allocation,
    OPCODE_abandonment,
    OPCODE_output,
    OPCODE_input,
    OPCODE_load_program,
    OPCODE_orthography 
} opcode;

typedef struct {
    platter * data;
    platter size;  /* size in bytes, not in elements */
} array;

struct machine_state { 
    platter registers[8];
    platter * finger;
    platter operation;
    opcode op;
    array array0;
};


/* allocates a buffer containing the program */
array read_program(char *filename)
{
    array ar={NULL,0};
    
    platter *buf=NULL;
    platter p=0;
    FILE *f;
    size_t size=0;  /*in bytes */

    unsigned char a,b,c,d;
    struct stat s;

    fprintf(stderr,"loading file: %s\n",filename);
    f=fopen(filename,"r");
    if (f==NULL) {
        fprintf (stderr,"failed to open file\n");
        exit (EXIT_FAILURE);
    }

    stat(filename,&s);
    if (s.st_size > 0) {
        fprintf(stderr,"detected file size: %lu\n",s.st_size);
        buf=malloc(s.st_size);
    } 

    while (!feof (f)) { 
        size += fread(&a,1,1,f); 
        size += fread(&b,1,1,f);
        size += fread(&c,1,1,f);
        size += fread(&d,1,1,f);
        
        p=(a<<24)+(b<<16)+(c<<8)+d;  /* this is necessary to override the defualt intel byte order */ 
        if (size > s.st_size)
            buf=realloc(buf,size); 
        buf[size/4 - 1]=p;
    } 

    ar.data=buf;
    ar.size=size;

    fclose(f);
    return ar;
}    

inline opcode decode_operation (platter op) 
{
    return op >> 28;
}


/**************************** Machine Operations ********************/
inline void do_conditional_move (struct machine_state *m, int a, int b, int c)
{
    /*
     * #0. Conditional Move.

                  The register A receives the value in register B,
                  unless the register C contains 0.  */

    if (m->registers[c] !=0)
        m->registers[a] = m->registers[b];
}

inline void do_array_index (struct machine_state *m, int a, int b, int c)
{
    /* #1. Array Index.

                  The register A receives the value stored at offset
                  in register C in the array identified by B.  */

    
    array *ar;

    if (m->registers[b]!=0)
    {
        ar=ARRAY(m->registers[b]);
        m->registers[a]=ar->data[m->registers[c]-1];
    }
    else
    {
        m->registers[a]=m->array0.data[m->registers[c]];
    }
}

inline void do_array_amendment (struct machine_state *m, int a, int b, int c)
{
    /* #2. Array Amendment.

                  The array identified by A is amended at the offset
                  in register B to store the value in register C. */

    if (m->registers[a]!=0)
        ARRAY(m->registers[a])->data[m->registers[b]]=m->registers[c];
    else
        m->array0.data[m->registers[b]]=m->registers[c];
}

inline void do_addition (struct machine_state *m, int a, int b, int c)
{
    /* #3. Addition.

                  The register A receives the value in register B plus 
                  the value in register C, modulo 2^32. */

    m->registers[a] = m->registers[b] + m->registers[c];
}

inline void do_multiplication (struct machine_state *m, int a, int b, int c)
{
    /* #4. Multiplication.

                  The register A receives the value in register B times
                  the value in register C, modulo 2^32. */

    m->registers[a] = m->registers[b] * m->registers[c];
}

inline void do_division (struct machine_state *m, int a, int b, int c)
{
    /* #5. Division.

                  The register A receives the value in register B
                  divided by the value in register C, if any, where
                  each quantity is treated treated as an unsigned 32
                  bit number. */

    m->registers[a] = m->registers[b] / m->registers[c];
}

inline void do_not_and (struct machine_state *m, int a, int b, int c)
{
    /* #6. Not-And.

                  Each bit in the register A receives the 1 bit if
                  either register B or register C has a 0 bit in that
                  position.  Otherwise the bit in register A receives
                  the 0 bit. */

    m->registers[a] = ~ (m->registers[b] & m->registers [c]);
}

inline void do_allocation (struct machine_state *m, int b, int c)
{
    /* #8. Allocation.

                  A new array is created with a capacity of platters
                  commensurate to the value in the register C. This
                  new array is initialized entirely with platters
                  holding the value 0. A bit pattern not consisting of
                  exclusively the 0 bit, and that identifies no other
                  active allocated array, is placed in the B register. */


	m->registers[b]=(platter)calloc (m->registers[c], sizeof (platter)); /* size is in bytes */
    fprintf(stderr,"allocated %d bytes to address %x\n",m->registers[c],m->registers[b]);
}

inline void do_abandonment (struct machine_state *m, int c)
{
    /* #9. Abandonment.

                  The array identified by the register C is abandoned.
                  Future allocations may then reuse that identifier. */

    assert(m->registers[c]!=0);
    fprintf(stderr,"abandoning address %x\n",m->registers[c]);
    free (ARRAY(m->registers[c])->data);
}

inline void do_output (struct machine_state *m, int c)
{
    /* #10. Output.

                  The value in the register C is displayed on the console
                  immediately. Only values between and including 0 and 255
                  are allowed. */

    putchar (m->registers[c]);
#if debug_output == 1
    putc(m->registers[c],stderr);
#endif

}

inline void do_input (struct machine_state *m, int c)
{
    /* #11. Input.

                  The universal machine waits for input on the console.
                  When input arrives, the register C is loaded with the
                  input, which must be between and including 0 and 255.
                  If the end of input has been signaled, then the 
                  register C is endowed with a uniform value pattern
                  where every place is pregnant with the 1 bit. */

    m->registers[c]=getchar ();
    if (m->registers[c] == (platter) EOF)
        m->registers[c] = 0xffffffff;
}

void do_load_program (struct machine_state *m, int b, int c)
{
    /* #12. Load Program.

                  The array identified by the B register is duplicated
                  and the duplicate shall replace the '0' array,
                  regardless of size. The execution finger is placed
                  to indicate the platter of this array that is
                  described by the offset given in C, where the value
                  0 denotes the first platter, 1 the second, et
                  cetera.

                  The '0' array shall be the most sublime choice for
                  loading, and shall be handled with the utmost
                  velocity. */

    if (m->registers[b] != 0) { /* if already the '0' array, don't allocate */
        free(m->array0.data); 

        m->array0.data = calloc(ARRAY(m->registers[b])->size,1);
        m->array0.size = ARRAY(m->registers[b])->size;
    }

    m->finger = m->array0.data + m->registers[c];
}

inline void do_orthography (struct machine_state *m, int a)
{
    /* #13. Orthography.

                  The value indicated is loaded into the register A
                  forthwith. */

    m->registers[a] = m -> operation & 0x01ffffff;
}
/****************************************** End of Operations *****************************/





inline void machine_step (struct machine_state * mstate)
{
    int a=0,b=0,c=0; /* used to specify which registers the ops use */

    mstate->operation = *(mstate->finger);
    mstate->op = decode_operation (mstate->operation);

    /* decode the registers to be used in this operation */
    if (mstate->op != OPCODE_orthography) {
        a=(mstate->operation) >> 6 & 07;
        b=(mstate->operation) >> 3 & 07;
        c=(mstate->operation) & 07;
    } else /* special register position on orthorgraphy operation */
        a=(mstate->operation) >> 25 & 07;

    mstate->finger++;

    switch (mstate->op) {
        case OPCODE_conditional_move: 
            do_conditional_move(mstate,a,b,c);
            break;
        case OPCODE_array_index: 
            do_array_index(mstate,a,b,c);
            break;
        case OPCODE_array_amendment: 
            do_array_amendment(mstate,a,b,c);
            break;
        case OPCODE_addition: 
            do_addition(mstate,a,b,c);
            break;    
        case OPCODE_multiplication: 
            do_multiplication(mstate,a,b,c);
            break;
        case OPCODE_division: 
            do_division(mstate,a,b,c);
            break;
        case OPCODE_not_and: 
            do_not_and(mstate,a,b,c);
            break;
        case OPCODE_halt: 
            break; /* do nothing */
        case OPCODE_allocation: 
            do_allocation(mstate,b,c); 
            break;
        case OPCODE_abandonment: 
            do_abandonment(mstate,c);
            break;
        case OPCODE_output: 
            do_output(mstate,c);
            break;
        case OPCODE_input: 
            do_input(mstate,c);
            break;
        case OPCODE_load_program: 
            do_load_program(mstate,b,c);
            break;
        case OPCODE_orthography: 
            do_orthography(mstate,a);
            break;
        default: 
            fprintf(stderr,"recieved unknown opcode 0x%x\n",mstate->op);
            exit (EXIT_FAILURE);
    }
}

int main(int argc,char *argv[])
{
    struct machine_state m = {{0},NULL,0,-1,{NULL,0}};


    if (argc != 2) {
        fprintf (stderr,"usage: %s filename\n",argv[0]);
        exit (EXIT_FAILURE);
    }


    m.array0=read_program(argv[1]); /* allocate a buffer containing the program */
    m.finger=m.array0.data;  /* initialize execution finger */

    /* "spin cycle" */
    while (m.op!=OPCODE_halt) {
        machine_step(&m);
    }
    
    free (m.array0.data);  /* free the array '0' */
    return EXIT_SUCCESS;
}    
