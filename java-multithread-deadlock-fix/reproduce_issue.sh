#!/bin/bash

# Compile the Java code
if [ ! -d "out" ]; then
  mkdir out
fi

echo "Compiling BankService..."
javac -d out src/BankService.java

if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

echo "Running BankService simulation..."
# Run the application
java -cp out BankService