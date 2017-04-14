#!/bin/bash

echo "";
echo "##################  TESTING THE CLIENT  ####################";
echo "";
echo "";

xterm -e 'python myclient.py localhost 7007 > test_1_output.txt'
 
diff test_1_expected.txt test_1_output.txt & export result=$?;

if [ $result -eq 0 ]
  then
    echo "ok"

xterm -e 'nc -l 20005 > test_1_output.txt'&
pid1=$!;   #  to get the pid of the latest opened process


echo "CREATING NC SERVER ON PORT 20005              --->        OK";
((success++))
echo "";

sleep 1;


# Client connects to the nc server with input test_1_input.txt
xterm -e 'python myclient.py localhost.localdomain 20005 toto < test_1_input.txt'&
pid2=$!;


echo "CLIENT CONNECT ON THE SERVER WITH INPUT       --->        OK";
((success++))
echo "";


sleep 1;   #  to get the pid of the latest opened process



# Testing if the output of the server is same as expected file?
diff test_1_expected.txt test_1_output.txt & export result=$?;

if [ $result -ne 0 ]
  then

    echo "##################  TESTING THE CLIENT  ####################";
    echo "-------------------       FAIL       -----------------------";
    echo "############# CLIENT IS NOT WORKING CORRECTLY ##############";
else
    echo "TESTING IF THE INPUT FILE = OUTPUT FILE       --->        OK";
    ((success++))
    echo "";
fi;
