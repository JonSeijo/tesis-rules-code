#generate_rules_multiple

import subprocess
import shlex

# family = "NEWAnk"
# clean_mode = "min"
# mr_types = ["ALL", "NE", "NN", "SMR"]
# min_lens = ["4", "5", "6", "7", "8"]
# supports = ["0.015", "0.020", "0.025", "0.030"]
# confidences = ["0.9"]
# max_time="30"

# family = "TPR1"
# clean_mode = "min"
# mr_types = ["ALL", "NE", "NN", "SMR"]
# min_lens = ["4"]
# supports = ["0.015", "0.020", "0.025", "0.030"]
# confidences = ["0.9"]
# max_time="30"

family = "LRR1"
clean_mode = "min"
mr_types = ["ALL", "NE", "NN", "SMR"]
min_lens = ["4"]
supports = ["0.015", "0.020", "0.025", "0.030"]
confidences = ["0.9"]
max_time="60"


for min_len in min_lens:
    for mr_type in mr_types:
        for support in supports:
            for confidence in confidences:
                # eg: NEWAnk_len7_NE_sub
                transaction_name = f"{family}_len{min_len}_{mr_type}_{clean_mode}"


                bash_command = f"./generate_rules.r --transactions_name={transaction_name} --min_support={support} --min_confidence={confidence} --max_time={max_time}"
                print(f"Running: {bash_command}")

                # https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
                subprocess.run(shlex.split(bash_command), check=True)

