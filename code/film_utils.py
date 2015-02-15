import numpy as np

def compare_submissions(f_a, f_b):
    f1 = open(f_a, "r")
    f2 = open(f_b, 'r')
    f1.readline()
    f2.readline()
    a = np.zeros((5, 5))
    while True:
        f1_line = f1.readline()
        f2_line = f2.readline()
        if f2_line == "":
            break
        
        f1_line = f1_line.split(",")
        f2_line = f2_line.split(",")

        a[int(float(f1_line[1]))][int(float(f2_line[1]))]+=1
    np.set_printoptions(suppress=True)
    print a
    return a
