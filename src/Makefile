CXX = $(shell wx-config --cxx)

TARGET = librecast
OBJECTS = $(TARGET).o ui/mainwindow.o

.SUFFIXES: .o .cpp

.cpp.o:
	$(CXX) -c `wx-config --cxxflags` -o $@ $<

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) -o ../bin/$(TARGET) $(OBJECTS) `wx-config --libs`

clean:
	rm -f *.o ../bin/$(TARGET)