CC=gcc
CXX=g++
TOPDIR=..
INCLUDE=${TOPDIR}/include
CFLAGS+=-std=c99
CXXFLAG+=-std=c++17

all: c_example cpp_example plo4_example omaha_example plo5_example plo6_example

c_example: c_example.c ../libpheval.a
	${CC} ${CFLAGS} -I${INCLUDE} $^ -o $@

cpp_example: cpp_example.cc ../libpheval.a
	${CXX} ${CXXFLAG} -I${INCLUDE} $^ -o $@

plo4_example: plo4_example.cc ../libphevalplo4.a
	${CXX} ${CXXFLAG} -I${INCLUDE} $^ -o $@

omaha_example: omaha_example.cc ../libphevalplo4.a
	${CXX} ${CXXFLAG} -I${INCLUDE} $^ -o $@

plo5_example: plo5_example.cc ../libphevalplo5.a
	${CXX} ${CXXFLAG} -I${INCLUDE} $^ -o $@

plo6_example: plo6_example.cc ../libphevalplo6.a
	${CXX} ${CXXFLAG} -I${INCLUDE} $^ -o $@

../libpheval.a:
	$(MAKE) -C ../ libpheval.a

../libphevalplo4.a:
	$(MAKE) -C ../ libphevalplo4.a

../libphevalplo5.a:
	$(MAKE) -C ../ libphevalplo5.a

../libphevalplo6.a:
	$(MAKE) -C ../ libphevalplo6.a

%.o: %.cc
	${CXX} -c ${CXXFLAG} -I${INCLUDE} $< -o $@

%.o: %.c
	${CC} -c ${CFLAGS} -I${INCLUDE} $< -o $@

clean:
	rm -f *.o c_example cpp_example plo4_example omaha_example plo5_example plo6_example
