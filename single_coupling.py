import subprocess
import os

couplings = [
    # "X10LL[1,1]",
    # "X10LL[2,1]",
    # "X10LL[3,1]",
    "X10LL[1,2]",
    # "X10LL[2,2]",
    # "X10LL[3,2]",
    # "X10LL[1,3]",
    # "X10LL[2,3]",
    # "X10LL[3,3]",
    # "X10RR[1,1]",
    # "X10RR[2,1]",
    # "X10RR[3,1]",
    # "X10RR[1,2]",
    # "X10RR[2,2]",
    # "X10RR[3,2]",
    # "X10RR[1,3]",
    # "X10RR[2,3]",
    # "X10RR[3,3]",
]

# couplings = ["Y10LL[1,3]"]


for i in range(len(couplings)):
    coup = couplings[i]
    # f = open(f"values/{coup}.csv", "a")
    # f.write("Mass\tLambda\tMin chi sq.\tChi Sq\tSigma \n")
    # f.close()
    # os.makedirs(f"values/{coupling}", exist_ok = True)
    for mass in range (1000, 5001, 100):
        output = f"""U1              # lepqtoquark model
{mass}			# mass
{coup}      # couplings
no				# ignore single and pair
2				# significance
0.1				# systematic error
0               # width constant
139000
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