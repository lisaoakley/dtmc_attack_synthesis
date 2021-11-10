# Modified from: https://github.com/prismmodelchecker/prism-api/blob/master/Makefile

# PRISM directory to link to
PRISM_DIR="../../prism"

# Path to py4j
PYJ_JAR="../env/share/py4j/py4j0.10.9.2.jar"

# Class to run
GATEWAY_MAINCLASS="io/github/lisaoakley/prism_gateway/PrismGateway"

# For compilation, just need access to classes/jars in the PRISM distribution AND py4j
DEPENDENCY_CLASSPATH="classes:$(PRISM_DIR):$(PRISM_DIR)/classes:$(PRISM_DIR)/lib/*:$(PRISM_DIR)/prism:$(PRISM_DIR)/prism/classes:$(PRISM_DIR)/prism/lib/*:$(PYJ_JAR)"

# This Makefile just builds all java files in src and puts the class files in classes

JAVA_FILES := $(shell cd src && find . -name '*.java')
CLASS_FILES = $(JAVA_FILES:%.java=classes/%.class)

default: all

all: init $(CLASS_FILES)

init:
	@mkdir -p classes

classes/%.class: src/%.java
	(javac -classpath $(DEPENDENCY_CLASSPATH) -d classes $<)

# Start server

start:
	PRISM_DIR=$(PRISM_DIR) GATEWAY_MAINCLASS=$(GATEWAY_MAINCLASS) ./run

# Test server connection

test:
	PRISM_DIR=$(PRISM_DIR) GATEWAY_MAINCLASS=$(GATEWAY_MAINCLASS) ./run
	@sleep 1
	@python example.py
	@pkill java

# Clean up

clean:
	@rm -f $(CLASS_FILES)

celan: clean
