this program accepts a file or path and searches for common patterns used in secrects that may be hard coded.

I provided the program with five patterns to look for. The prgram is designed to be used with argparse so that it can be ran from the command line.
The program takes in the path or file provided in the command line and checks to see if it exists. 
If the file exsists it starts the scan. If it is a directory, the program goes through the tree and scans each file.
The scan function reads each file line by line and numbers each line for logging. It checks for the patterns and prints if one is found. 
The program also prints out a warning if it cannot read the file. 
