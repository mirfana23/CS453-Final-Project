rm -rf ./generated_input/dummy1/
# timeout -s 2 $1 python main.py -t target/dummy1.py -i init_seed/dummy1/ -s ./generated_input/dummy1/
timeout -s 2 60s python main.py -t target/dummy1.py -i init_seed/dummy1/ -s ./generated_input/dummy1/