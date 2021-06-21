import os
import subprocess
import argparse
import sys
from Fuzzer import RandomFuzzer, Runner
from Delta_Debugging import DeltaDebuggingReducer

def fault_percentage(DDres, Failres):
    return len(DDres) / len(Failres)

class MysteryRunner(Runner):
        def run(self, inp):
            inp_list = list(inp.strip())
            for i in range(0, len(inp_list)):
                inp_list[i] = int(inp_list[i])
            false_cmd = "python3 %s %s" %(target_program, str(inp_list))
            falseres = subprocess.check_output(false_cmd, text=True, shell=True)
            print("=======")
            true_cmd = "python3 %s %s" %(ref_program, '"' + str(inp_list) + '"')
            trueres = subprocess.check_output(true_cmd, text=True, shell=True)
            if falseres == trueres:
                return inp, Runner.PASS
            else:
                return inp, Runner.FAIL
mystery = MysteryRunner()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Compare Fuzzer')
	parser.add_argument('-t', '--target', type=str, required = True)
	parser.add_argument('-r', '--reference', type=str, required = True)
	parser.add_argument('-b', '--base_dir', type=str, required = True)
	parser.add_argument('-p', '--proposed_dir', type=str, required = True)
	args = parser.parse_args()
	target_program = args.target
	ref_program = args.reference
	 
	# 0. check for error
	if not os.path.exists(target_program):
		print("Target program %s does not exists" %(target_program))
		sys.exit()
	elif not os.path.isfile(target_program) or not target_program[-len(".py"):] == ".py":
	    print("Target program %s not a python script" %(target_program))
	if not os.path.exists(ref_program):
		print("Target program %s does not exists" %(ref_program))
		sys.exit()
	elif not os.path.isfile(ref_program) or not ref_program[-len(".py"):] == ".py":
	    print("Target program %s not a python script" %(ref_program))
	
	
	dirbase = args.base_dir
	dirprop = args.proposed_dir
	base_seed = []
	proposed_seed = []

	# 2. access the fuzzer testcase
	maindir = os.getcwd()
	pathname = ""
	for file in os.listdir(dirbase):
		pathname = os.path.join(dirbase, file)
		dirfile = open(pathname, 'r')
		lines = dirfile.readlines()
		content = "".join(lines)
		base_seed.append(content.strip())
	for file in os.listdir(dirprop):
		pathname = os.path.join(dirprop, file)
		dirfile = open(pathname, 'r')
		lines = dirfile.readlines()
		content = "".join(lines)
		proposed_seed.append(content.strip())
	
	base_pfi = []
	proposed_pfi = []

	# 3. reduce the testcase
	for test in base_seed:
		print("aa")
		result, outcome = mystery.run(test)
		print("bb")
		if(outcome == mystery.FAIL):
			dd_reducer = DeltaDebuggingReducer(mystery, log_test=False)
			ddres = dd_reducer.reduce(result)
			pfires = fault_percentage(ddres, result)
			base_pfi.append(pfires)
	print("============")
	for test in proposed_seed:
		print("aa")
		result, outcome = mystery.run(test)
		print("bb")
		if(outcome == mystery.FAIL):
			dd_reducer = DeltaDebuggingReducer(mystery, log_test=False)
			ddres = dd_reducer.reduce(result)
			pfires = fault_percentage(ddres, result)
			proposed_pfi.append(pfires)
	
	
	# 4. calculate and present the calculated pfi
	base_avg_pfi = 100*sum(base_pfi)/len(base_pfi)
	prop_avg_pfi = 100*sum(proposed_pfi)/len(proposed_pfi)
	print("Average percentage of fault inducing input (baseline fuzzer) : %.2f%%" %(base_avg_pfi))
	print("Average percentage of fault inducing input (proposed fuzzer) : %.2f%%" %(prop_avg_pfi))
	

	

