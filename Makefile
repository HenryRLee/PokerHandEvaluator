CC=gcc

all: five six seven

five: test/five.o src/libeval5.a
	${CC} ${CFLAGS} $^ -o $@

six: test/six.o src/libeval6.a
	${CC} ${CFLAGS} $^ -o $@

seven: test/seven.o src/libeval7.a
	${CC} ${CFLAGS} $^ -o $@

src/libeval5.a: src/evaluator5.o src/hash.o src/hashtable.o src/hashtable5.o src/dptables.o
	ar rcs $@ $^

src/libeval6.a: src/evaluator6.o src/hash.o src/hashtable.o src/hashtable6.o src/dptables.o
	ar rcs $@ $^

src/libeval7.a: src/evaluator7.o src/hash.o src/hashtable.o src/hashtable7.o src/dptables.o
	ar rcs $@ $^

%.o: %.c
	${CC} -c ${CFLAGS} $< -o $@

clean:
	rm -f src/*.o test/*.o *.o src/*.a five seven

