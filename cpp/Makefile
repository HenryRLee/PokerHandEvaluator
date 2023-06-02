CC=gcc
CXX=g++
INCLUDE=./include
CFLAGS+=-O2 -std=c99
CXXFLAGS+=-O2 -std=c++17

all: libpheval.a libphevalomaha.a libphevalplo5.a

libpheval.a: src/evaluator5.c.o src/hashtable5.c.o \
             src/evaluator6.c.o src/hashtable6.c.o \
             src/evaluator7.c.o src/hashtable7.c.o \
             src/hash.c.o src/hashtable.c.o src/dptables.c.o src/evaluator.cc.o src/hand.cc.o \
             src/rank.c.o src/7462.c.o
	ar rcs $@ $^

libphevalomaha.a: src/dptables.c.o src/tables_omaha.c.o \
                  src/evaluator_omaha.c.o src/evaluator_omaha.cc.o \
                  src/hash.c.o src/hand.cc.o \
                  src/hashtable.c.o src/rank.c.o \
                  src/7462.c.o
	ar rcs $@ $^

libphevalplo5.a: src/dptables.c.o src/tables_plo5.c.o \
                 src/evaluator_plo5.c.o src/evaluator_plo5.cc.o \
                 src/hash.c.o src/hand.cc.o \
                 src/hashtable.c.o src/rank.c.o \
                 src/7462.c.o
	ar rcs $@ $^

%.c.o: %.c
	${CC} -c ${CFLAGS} -I${INCLUDE} $< -o $@

%.cc.o: %.cc
	${CXX} -c ${CXXFLAGS} -I${INCLUDE} $< -o $@

clean:
	rm -f src/*.o libpheval.a libphevalomaha.a libphevalplo5.a
