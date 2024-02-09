#!/usr/bin/env python

# plot-stack.py  
# plot a set of csv files, each containing one column of data
# in this case, energy spectrum from OpenGamma scintillator board
# J.Beale 9-Feb-2024

import os
import sys           # command-line args
import glob          # combine set of files
import pandas as pd
import matplotlib.pyplot as plt

def plot_all_csv(directory_path):
    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

    if not csv_files:
        print(f"No .csv files in directory: {directory_path}")
        return

    dfs = []  # empty list of dataframes
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, header=0, comment="#", names=[f'Values_{os.path.basename(csv_file)}'])
            dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f"Skipping empty CSV file: {csv_file}")
        except pd.errors.ParserError:
            print(f"Error parsing CSV file at {csv_file}.")

    if not dfs:
        print("No valid data found in files.")
        return

    combined_df = pd.concat(dfs, axis=1) # combine and plot all frames
    combined_df.plot()

    plt.title('stacked spectrums')
    plt.xlabel('channel')
    plt.ylabel('counts')
    plt.gca().get_legend().remove()
    plt.yscale('log')
    plt.grid(visible=True, linestyle="dotted", color="gray")
    plt.show()

# ----------------------------------------------------------------------
if __name__ == "__main__":
        
    if len(sys.argv) != 2:
        print("Usage: plot-stack.py <directory>")
    else:
        try:
            dir = sys.argv[1]
            plot_all_csv(dir)
        except Exception as e:
            print(f"Error: {e}")
