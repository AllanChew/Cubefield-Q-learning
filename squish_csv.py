import csv

# example usage: squish_csv("trial_results.csv","squished_results.csv",3)
#   this will keep 1/3 of the original rows
def squish_csv(in_fname="input.csv",out_fname="squished_results.csv",skip=2):
    infile = open(in_fname, "r")
    outfile = open(out_fname,"w")
    ctr = -1
    s = infile.readline()
    while s != "":
        if ctr <= 0:
            outfile.write(s)
        ctr = (ctr + 1) % skip
        s = infile.readline()
    infile.close()
    outfile.close()
