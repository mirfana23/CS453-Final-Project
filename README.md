# CS453-Final-Project

This is our github repository for the automated software testing final project

0. Edit target program and its reference. 
The current target program only has the function definition of the program. Make sure to include a main function as needed to capture the output of the program. The target program is located at the target folder in the main directory, baseline folder, and the proposed folder. Subsequently the reference program is located at the ref folder in the main directory and the proposed folder.

1.run baseline fuzzer
Edit the runfuzz.sh as specified to the target program and the base seed. Some base seed have to be parsed depending on the program. Make sure to specify the the name of the folder to store the test cases. the valid input would be placed in the subfolder "input" and the crash input would be placed in subfolder "crash".

2. run proposed test case generation
run the main.py on proposed folder and specify the target program and its reference.

3. compare the results
run the maincounter.py on main directory, and specify the folder that contains both baseline and proposed test cases, as well as the target program and its reference.
