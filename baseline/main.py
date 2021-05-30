import os
import sys
import signal
import argparse
import subprocess

from inpfuzzer import InputFuzzer
from pysrunner import ScriptRunner

# DEBUG_MODE = bool(os.environ.get("DEBUG", 0))
# DEBUG_MODE = True
# def print_DEBUG_LOG(*strlog):
# 	if DEBUG_MODE:
# 		strstrlog = [str(strl) for strl in strlog]
# 		print(" ".join((strstrlog)))

input_fuzzer = InputFuzzer([])
input_save_dir = ""

def signal_handler(sig, frame):
    global input_save_dir
    global input_fuzzer
    os.makedirs(input_save_dir)
    print("SAVE THE GENERATED INPUT TO '{}'".format(input_save_dir))
    input_fuzzer.save_input(input_save_dir)
    sys.exit(0)

def command_error(*strlog):
    strstrlog = [str(strl) for strl in strlog]
    # print(" ".join((strstrlog)))
    sys.exit(*strlog)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='Baseline Fuzzer')
    # parser.add_argument('-a', '--action', choices=["mutate", "execute"], required=True)
    parser.add_argument('-t', '--target', type=str, required=True)
    parser.add_argument('-i', '--initial_seed_dir', type=str, required=True)
    parser.add_argument('-s', '--save_dir', type=str, required=True)
    # parser.add_argument("remaining", nargs="*")

    args = parser.parse_args()

    target_program = args.target
    # prog_args = args.remaining
    init_seed_dir = args.initial_seed_dir

    # Preparing 
    if not os.path.exists(target_program):
        command_error("Target program '{}' is not exists".format(target_program))
    elif not os.path.isfile(target_program) or not target_program[-len(".py"):] == ".py":
        print(target_program[:-len(".py")])
        command_error("Target program '{}' is not a python script".format(target_program))
    pyscript_runner = ScriptRunner(target_program)
    pyscript_runner.erase_cov()

    # 1. read the initial seed files 
    if not os.path.exists(init_seed_dir):
        command_error("Initial seed directory '{}' is not exists".format(init_seed_dir))
    elif not os.path.isdir(init_seed_dir):
        command_error("Target program '{}' is not a directory".format(init_seed_dir))
    init_seed = []
    for init_f in os.listdir(init_seed_dir):
        init_f_path = os.path.join(init_seed_dir, init_f)
        if os.path.isfile(init_f_path):
            	with open(init_f_path, 'r') as init_f_file:
                    lines = init_f_file.readlines()
                    init_f_content = "".join(lines)
                    init_seed.append(init_f_content.strip())
    # print(init_seed)

    # 2. run the initial seed 
    input_fuzzer.reinit(init_seed)
    for init_inp in input_fuzzer.input_queue_set:
        pyscript_runner.run([init_inp])

    # 3. save directory
    input_save_dir = args.save_dir

    # 4. start fuzzing
    i = 0
    print("START TO RUN THE FUZZER")
    while True:
        new_input = input_fuzzer.get_fuzzed_input()
        pass_fail, raise_cov, total_cov = pyscript_runner.run_check([new_input])
        if pass_fail == ScriptRunner.FAIL:
            input_fuzzer.add_crash(new_input)
        elif raise_cov:
            input_fuzzer.add_input(new_input)
        print("#{} - input:'{}' - total_cov:{}".format((i+1), new_input, total_cov))
        i += 1
