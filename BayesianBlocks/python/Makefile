SWIG = swig
#SWIG_DIR = /scratch/local
#PYINCLUDE = -I$(GLAST_EXT)/python/2.3/Linux/include
#PYINCLUDE = -I/usr/local/include/python2.3

CFLAGS = -g 

INCLUDE = -I$(BAYESIANBLOCKSROOT)

LIBS = -L ../$(BINDIR)/ -lBayesianBlocks

#LIBS = -L$(SWIG_DIR)/lib -lswigpy

module_base = BayesianBlocks
module_name = _${module_base}.so

${module_name}: ${module_base}_wrap.o
	${CXX} -shared $< ${LIBS} -o ${module_name}

${module_base}_wrap.o: ${module_base}_wrap.cxx
	${CXX} -c ${CFLAGS} ${INCLUDE} -I${PYINCLUDE} -o $@ $<

${module_base}_wrap.cxx: ${module_base}.i
	${SWIG} -python -c++ ${module_base}.i

%.o: %.cxx
	${CXX} -c ${CFLAGS} $<

anew:
	make clean
	make

tar_file:
	tar cvf ${MY_PROG}.tar ${SRCS} ${HFILES} ${OTHER_FILES} ${srcs}

clean:
	/bin/rm -f *~
	/bin/rm -f *.o
	/bin/rm -f *.trace
	/bin/rm -f *wrap*
	/bin/rm -f *.so
	/bin/rm -f ${module_base}.py*
	/bin/rm -f ${module_base}.cxx

very_clean:
	make clean
	/bin/rm -f core
	/bin/rm -f _${module_base}.so

gammln: gammln.i
	gcc -c gammln.c -o gammln.o
	swig -python gammln.i
	gcc -c gammln_wrap.c -I/usr/local/include/python2.3
	ld -shared gammln.o gammln_wrap.o -o _gammln.so
