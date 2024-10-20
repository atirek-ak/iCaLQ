import os
import matplotlib.pyplot as plt

# Define colors for different conditions
colors = {'blue': 'blue', 'brown': 'brown'}

# Function to parse the data and plot
def plot_data(filename):
    plt.clf()
    with open(filename, 'r', encoding='latin-1') as file:
        for line in file:
            # Split the line by comma
            # double coupling
            data = line.strip().split(',')
            if len(data) == 5:
                x = float(data[0])
                y = float(data[1])
                # difference = float(data[2]) - float(data[1])
                # print(data[5])
                # print(type(data[5]))
                if data[4].strip() == "1":
                    plt.plot(x, y, 'o', color=colors['blue'])
                # elif data[5].strip() == "2":
                #     plt.plot(x, y, 'o', color=colors['brown'])
            # single coupling
            if  len(data) == 4:
                x = float(data[0])
                y = float(data[3])
                difference = float(data[2]) - float(data[1])
                if difference < 1:
                    plt.plot(x, y, 'o', color=colors['blue'])
                elif difference < 4:
                    plt.plot(x, y, 'o', color=colors['brown'])
                    
    # Add labels and show plot
    plt.xlabel('Leptoquark mass')
    plt.ylabel('Coupling value')
    plt.title('Single coupling values plot')
    # plt.show()
    plt.savefig(f"plots/{os.path.basename(filename)}.png")

# Example usage
directory = "plots/data"

# Iterate over all files in the directory
for filename in os.listdir(directory):
#     # Check if the file is a regular file (not a directory)
    if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".csv"):
        plot_data(os.path.join(directory, filename))
#     # break

# plot_data(directory, "X10LL[1,1].csv")