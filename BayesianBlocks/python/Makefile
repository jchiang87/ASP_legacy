SWIG = swig
#SWIG_DIR = /scratch/local
#PYINCLUDE = -I$(GLAST_EXT)/python/2.3/Linux/include
#PYINCLUDE = -I/usr/local/include/python2.3

CFLAGS = -g 

INCLUDE = -I$(BAYESIANBLOCKSROOT)\
	-I$(ASTROROOT)\
	-I$(LATRESPONSEROOT)\
	-I$(LIKELIHOODROOT)\
	-I$(CLHEP_DIR)/1.8.0.0/include

LIBS = -L ../$(BINDIR)/ -lBayesianBlocks\
	-L$(LATRESPONSEROOT)/$(BINDIR) -llatResponseLib\
	-L$(LIKELIHOODROOT)/$(BINDIR) -lLikelihoodLib\
	-L$(ST_APPROOT)/$(BINDIR) -lst_appLib\
	-L$(MAP_TOOLSROOT)/$(BINDIR) -lmap_toolsLib\
	-L$(ASTROROOT)/$(BINDIR) -lastro\
	-L$(OPTIMIZERSROOT)/$(BINDIR) -loptimizersLib\
	-L$(HOOPSROOT)/$(BINDIR) -lhoopsLib\
	-L$(GLAST_EXT)/pil/1.9.2/lib/linux-3.2 -lpil\
	-L$(TIPROOT)/$(BINDIR) -ltipLib\
	-L$(XMLROOT)/$(BINDIR) -lxml\
	-L$(FACILITIESROOT)/$(BINDIR) -lfacilities\
	-L$(CFITSIO_DIR)/lib -lcfitsio\
	-L$(CLHEP_DIR)/1.8.0.0/lib -lCLHEP\
	-L$(GLAST_EXT)/xerces/1.7.0/lib/ -lxerces-c1_7_0 -lpthread\
	-L$(GLAST_EXT)/ROOT/v3.10.02/root/lib\
	-lCore -lCint -lTree -lMatrix -lPhysics\
	-lHist -lGraf -lGraf3d -lGpad -lRint -lPostscript\
	-lg2c -L$(SWIG_DIR)/lib -lswigpy -fPIC -ldl

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
