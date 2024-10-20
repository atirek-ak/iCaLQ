import subprocess
import numpy as np

couplings = [
#    ["X10LL[3,1]", "X10RR[1,1]"],
#    ["X10LL[3,1]", "X10RR[2,1]"],
#    ["X10LL[3,1]", "X10RR[3,1]"],
#    ["X10LL[3,2]", "X10RR[1,2]"],
#    ["X10LL[3,2]", "X10RR[2,2]"],
   ["X10LL[3,2]", "X10RR[3,2]"],
#    ["X10LL[3,3]", "X10RR[1,3]"],
#    ["X10LL[3,3]", "X10RR[3,3]"],
#    ["X10RR[1,3]", "X10RR[3,3]"],
#    ["X10LL[2,2]", "X10RR[2,2]"],
]

# couplings = [
#     ["Y10LL[2,2]", "Y10RR[2,2]"]
#     ]

# update values
with open("sample/sample_1.vals", "w") as f:
    for i in np.arange(-3.5, 3.5, 0.1):
        for j in np.arange(-3.5, 3.5, 0.1):
            f.write(f"{i} {j}\n")


for i in range(len(couplings)):
    coup = couplings[i]
    for mass in range (2500, 2501, 10000):
        output = f"""U1              # lepqtoquark model
{mass}			# mass
{coup[0]}  {coup[1]}    # couplings
no				# ignore single and pair
2				# significance
0.1				# systematic error
0               # width constant
139
0
"""
        # update sample_1.card
        f = open("sample/sample_1.card", "w")
        f.write(output)
        f.close()
        

        rc = subprocess.call("./sample_1.sh", shell=True)
        max_lambda_val = subprocess.check_output(['tail', '-1', "sample/sample_1_yes.csv"]).decode("utf-8").split(',')[0]
        # f = open(f"values/{coup}.csv", "a")
        # f.write(f"{mass}, {max_lambda_val} \n")
        # f.close()
        # print(f"{mass}, {max_lambda_val} done")