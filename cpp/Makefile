CC=gcc
CXX=g++
INCLUDE=./include
CFLAGS+=-Ofast
CXXFLAGS+=-Ofast -std=c++14

all: libpheval.a

libpheval.a: src/evaluator5.o src/hashtable5.o \
             src/evaluator6.o src/hashtable6.o \
             src/evaluator7.o src/hashtable7.o \
             src/evaluator8.o src/hashtable8.o \
             src/evaluator9.o src/hashtable9.o \
             src/hash.o src/hashtable.o src/dptables.o src/evaluator.o
	ar rcs $@ $^

%.o: %.c
	${CC} -c ${CFLAGS} -I${INCLUDE} $< -o $@

%.o: %.cc
	${CXX} -c ${CXXFLAGS} -I${INCLUDE} $< -o $@
