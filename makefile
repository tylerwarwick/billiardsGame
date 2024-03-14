## Declare compiler
CC = clang

## Declare compile flags
CFLAGS = -std=c99 -Wall -pedantic

## Linker flags (need this to create shared library object file)
LDFLAGS = -shared

## Shared libray name
TARGET = libphylib.so

## Source file
SRC = phylib.c

## Object File
OBJ = phylib.o

##What are we trying to achieve
all : $(TARGET) $(OBJ) phylib_wrap.o _phylib.so phylib.py phylib_wrap.c 

## Compile shared library
$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) $(OBJ) -o $(TARGET) -lm

## Compile standard object file from source file
##fPIC flag makes "position independent" object file which is important for shared libraries
## $< and $@ refer to the dependencies and the target
$(OBJ) : $(SRC)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

## A2 SECTION
## Phylib_wrap object file
phylib_wrap.o : phylib_wrap.c
	$(CC) $(CFLAGS) -c $< -I/usr/include/python3.11/ -fPIC -o $@

# SWIG Command
phylib.py phylib_wrap.c : phylib.i
	swig -python phylib.i

## _phylib shared object file
_phylib.so : phylib_wrap.o
	$(CC) $(CFLAGS) $(LDFLAGS) $< -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o $@


## Remove all object and shared files.
clean:
	rm -f *.o *.so