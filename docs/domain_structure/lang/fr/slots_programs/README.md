Slot program file are executable files.
Slot lists are great if your slot values always stay the same and are easily written out by hand. 
If you have slot values that you need to be generated each time Haroun is trained, you can use slot programs.
To create a slot program, create a file with the name you wish your slot to be create.
Write a program in this file, such as a bash script or python script. 
Make sure to include the shebang and mark the file as executable.

Your program must print the content of the slot file you want to create.

Exemple : color.sh

#!/usr/bin/env bash
echo 'red'
echo 'green'
echo 'blue'