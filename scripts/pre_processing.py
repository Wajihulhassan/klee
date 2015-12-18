import sys
import subprocess
import math
import re

def find_declaration(line):
    if re.search(".*int.*", line, flags = 0) != None or re.search(".*klee_make_symbolic.*", line, flags = 0):
        return True
    else:
        return False

def find_condition(line):
    if re.search(".*if.*(.*).*{", line, flags = 0) != None:
        return True
    else:
        return False

def condition_end(line):
    if re.search(".*}.*", line, flags = 0) != None:
        return True
    else:
        return False

def add_random_condition(fil):
    fil.write("if(true) {\n")
    fil.write("assert(true);\n")

def add_condition_end(fil):
    fil.write("}\n")
    
if __name__ == "__main__":
    
    v2 = sys.argv[2]
    v1 = sys.argv[1]
    diff_print = subprocess.Popen("diff " + v1 + " " + v2, shell=True, stdout=subprocess.PIPE).stdout.read()
    diff_l = diff_print.split("\n")[1:]
    l = []
    with open(v1) as fil1:
        l.append(fil1.readlines())

    with open(v2) as fil2:
        l.append(fil2.readlines())
        
    with open(v1 + "_new", "w+") as new_fil1:
        with open(v2 + "_new", "w+") as new_fil2:
            if len(l[0]) == len(l[1]):
                for line in l[0]:
                    new_fil1.write(line)
                for line in l[1]:
                    new_fil2.write(line)
                
            pass
            #skip include and function name
            p = [2, 2]
            pd = 1
            while p[0] < len(l[0]) and p[1] < len(l[1]):
                if l[0][p[0]] == l[1][p[1]]:
                    new_fil1.write(l[0][p[0]])
                    new_fil2.write(l[1][p[1]])
                    p[0] += 1
                    p[1] += 1
                else:
                    while p[0] < len(l[0]) and p[1] < len(l[1]) and l[0][p[0]] != l[1][p[1]]:
                        less = 0
                        more = 1
                        new_less_file = None
                        new_more_file = None
                        #v2 is more
                        if diff_l[pd][0] == '>':
                            new_less_file = new_fil1
                            less = 0
                            more = 1
                            new_more_file = new_fil2
                        else:
                            less = 1
                            more = 0
                            new_less_file = new_fil2
                            new_more_file = new_file1

                        #found declaration
                        if find_declaration(l[more][p[more]]):
                            new_less_file.write(l[more][p[more]][1:])
                        #found new condition
                        elif find_condition(l[more][p[more]]):
                            add_random_condition(new_less_file)
                        elif condition_end(l[more][p[more]]):
                            add_condition_end(new_less_file)

                        new_more_file.write(l[more][p[more]][1:])
                        p[more] += 1
                        pd += 1
                    
                            
                        
                    
