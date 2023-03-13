# Makefile for tx-generator

# options
CC						= g++
#CXX						= g++
#OUTPUT_OPTION	= -o $@
#CFLAGS				= -O3 -fomit-frame-pointer
XXFLAGS			= -O3 -fomit-frame-pointer 
CPPFLAGS			= -O3 -Wall -DNDEBUG 
LDFLAGS				= 
LDLIBS				= 
#TARGET_ARCH		=

# targets
.PHONY: all
all: tx-generator
tx-generator: sais.o FastaElement.o Tools.o txmers.o tx-generator.o

distclean: clean
clean:
	$(RM) tx-generator familiartyChart.o txmers.o FastaElement.o Tools.o sais.o 

# dependencies
sais.o FastaElement.o Tools.o txmers.o tx-generator.o: sais.h FastaElement.h Tools.h txmers.h Makefile
