To run the code you need to use the PRISM Java API, made available to Python through the Py4J Java Server. Instructions on how to start the server are listed below. Some versions of PRISM are not supported. Experiments in the original paper were run using PRISM source code at sha e70e0f3b5567c073633f6afc57d5a6318b04726d ([this commit](https://github.com/prismmodelchecker/prism/commit/e70e0f3b5567c073633f6afc57d5a6318b04726d))

## Install Py4J
Install [py4j](https://www.py4j.org/install.html) and make sure the Makefile is referencing the correct version and filepath of the py4j jar.

## Compile
```
make
```

## Start Server
```
make start
```

## Optional: Test Server
```
make test
> 0.5
```

## Troubleshooting
If you get an error: `error: method does not override or implement a method from a supertype`, make sure you have specified `PRISM_DIR` in the Makefile to a directory which contains a `prism/classes` directory with the compiled PRISM code.

If you get an error:
`error: cannot find symbol GatewayServer server = new GatewayServer(gw);` make sure you have specified the `PYJ_JAR` in the Makefile to reference the correct filepath of the py4j jar (more details here: https://www.py4j.org/install.html).
  
If you get the error `No module named py4j.java_gateway` make sure that you have installed the python py4j package (more details here: https://www.py4j.org/install.html).

If you get further errors, try compiling PRISM from [this commit](https://github.com/prismmodelchecker/prism/commit/e70e0f3b5567c073633f6afc57d5a6318b04726d) (sha e70e0f3b5567c073633f6afc57d5a6318b04726d).