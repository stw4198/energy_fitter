SHELL = /bin/sh
NAME = all
MAKEFILE = Makefile
ifeq ($(MAKECMDGOALS),)
	ERROR_RESULT:=$(error "No executable name provided: make (name)")
endif

RAT_LIBS = -L$(RATROOT)/lib -lRATEvent -lRATPAC -L$(ROOTSYS)/lib -lCore -lRIO -lTree -lPhysics -lMathCore
ROOT_FLAG = `root-config --cflags --libs`


LIBRARIES  := $(LIBRARIES) -L$(ROOTSYS)/lib -L$(RATROOT)/lib $(RAT_LIBS)

INCLUDES := $(INCLUDES) -I$(RATROOT)/include -I$(ROOTSYS)/include


all: $(MAKECMDGOALS)

$(MAKECMDGOALS): $(OBJS) $(MAKECMDGOALS).cc
	$(CXX) -o $(MAKECMDGOALS) $(CXXFLAGS) $(LDFLAGS) $(MAKECMDGOALS).cc -g $(ROOT_FLAG) $(INCLUDES) $(OBJS) $(LIBRARIES)

%.o : %.cc
	g++ $(ROOT_FLAG) $(RAT_LIBS) -c $*.cc
#################### CLEANING


clean:
	$(RM) *.o *~ core 
	$(RM) $(MAKECMDGOALS)

