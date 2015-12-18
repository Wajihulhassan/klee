import sys
import subprocess
import os.path
import re
import time

TEST_DIR = "test1/"
TABLE_OUTPUT = "/home/klee/paper527/tables/table1.tex"
NUM_TESTS = 1

def create_combined_fil(i):
    #print("python pre_processing.py " + TEST_DIR + "testbase.c " + TEST_DIR + "test" + str(i) + ".c")
    #p = subprocess.Popen(["python", "pre_processing.py",  TEST_DIR + "test0.c", TEST_DIR + "test" + str(i) + ".c"])
    #p.wait()
    
    with open(TEST_DIR + "test" + str(i) + "_combined.c", "w") as combined_fil:
        combined_fil.write("#include <klee/klee.h>\n")
        with open(TEST_DIR + "testbase.c") as old_fil:
            for line in old_fil.readlines():
                combined_fil.write(line);
        with open(TEST_DIR + "test" + str(i) + ".c") as new_fil:
            for line in new_fil.readlines():
                combined_fil.write(line);
        combined_fil.write("int main(int argc, char** argv){\n");
        combined_fil.write("int g = func_2();");
        combined_fil.write("return g;\n");
        combined_fil.write("}");

def run(i):
    print("Compile")
    p = subprocess.Popen(["llvm-gcc", "-I", "../include", "--emit-llvm", "-c", "-g", TEST_DIR + "test" + str(i) + "_combined.c"])
    p.wait()
    p = subprocess.Popen(["mv", "test" + str(i) + "_combined.o", "/tmp/linked_klee.o"])
    p.wait()
    p = subprocess.Popen(["rm", "-rf", "klee-out-*"])
    p.wait()
    #Run without directed search
    start = time.time()
    print("Run klee")
    output = subprocess.Popen(["klee","-search", "Directed", "/tmp/linked_klee.o"], shell = True, stdout = subprocess.PIPE).stdout.read()
    #p.wait()
    print("KLEE run finished")
    end = time.time()
    #output = p.stdout.read()
    g = re.match("KLEE: done: total instructions = .*")
    total_states = g.group().split(" = ")[1].strip("\n")
    g = re.match("KLEE: done: completed paths = .*")
    total_PCs = g.group().split(" = ")[1].strip("\n")
    elapse_time = round((end - start) * 1000, 0)
    return total_states, total_PCs, elapse_time

def write_output(total_states, total_PCs, elpase_time, i, output):
    version = None
    if i == 0:
        version = "Base"
    elif i > NUM_TESTS:
        version = "Avg."
    else:
        version = "Mutant " + str(i)
    
    output.write(version + " & " + total_states + " & " + total_PCs + " & " + str(elapse_time) + " \\\n")

def finish_table(output):
    output.write("\midrule\n")
    output.write("\end{tabular}\n")
    output.write("\end{small}\n")
    output.write("\end{figure}\n")

def initiate_table(output):
    output.write("\begin{figure*}[tb]\n")
    output.write("\begin{small}\n")
    output.write("\begin{tabular}{rrrr}\n")
    output.write("\toprule\n")
    output.write("version & \# of states & \# of PCs & elapsed time (ms)\\\n")
    output.write("\midrule\n")

def calculate_avg(rows):
    states = 0
    PCs = 0
    time = 0.0
    for i in range(1, len(rows)):
        states += int(rows[i][0])
        PCs += int(rows[i][1])
        time += int(rows[i][2])

    states = round(states * 1.0 / NUM_TESTS, 0)
    PCs = round(PCs * 1.0 / NUM_TESTS, 0)
    time = round(time * 1.0 / NUM_TESTS, 0)
    return states, PCs, time

if __name__ == "__main__":
    '''
    for i in range(0, NUM_TESTS + 1):
        create_combined_fil(i)
    '''
    with open(TABLE_OUTPUT, "w") as output:
        initiate_table(output)
        rows = []
        create_combined_fil(0)
        total_states, total_PCs, elapse_time = run(0)
        rows.append((total_states, total_PCs, elapse_time))
        for i in range(1, NUM_TESTS + 1):
            if not os.path.exists(TEST_DIR + "test" + str(i) + ".c"):
                #create_combined_fil(i)
                total_states, total_PCs, elapse_time = run(i)
                rows.append((total_states, total_PCs, elapse_time))
        
        for i in len(rows):
            write_output(rows[i][0], rows[i][1], rows[i][2], i, output)
    
        total_states, total_PCs, elapse_time = calculate_avg(rows)
        write_output(total_states, total_PCs, elapse_time, NUM_TESTS + 1, output)
        finish_table(output)

