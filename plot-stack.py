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
    csv_files = glob.glob(os.path.join(directory_path, '*_spec.csv'))

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

    df = pd.concat(dfs, axis=1)  # combine and plot all frames
    hours = len(df.columns)      # each column was accumulated over 1 hour
    df['mean'] = df.mean(axis=1) # create new column with row-average of all existing cols
    
    fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1)        
        
    # print(df['mean'])
    df['mean'].plot(ax=ax1)
    #plt.plot(df['mean'])
    
    sTitle = ("Spectrum Avg: %d hours" % hours)
    ax1.set_title(sTitle)
    ax1.set_xlabel('channel')
    #ax1.set_ylabel('counts')
    ax1.set_yscale('log')
    ax1.grid(visible=True, linestyle="dotted", color="gray")
    ax1.axis(ymin=1)
    #plt.show()
    #return
    
    df.plot(ax=ax2)    
    #sTitle = ("Spectrum Sequence: %d hours" % hours)
    #ax2.set_title(sTitle)
    ax2.set_xlabel('channel')
    ax2.set_ylabel('counts')
    ax2.set_yscale('log')
    ax2.grid(visible=True, linestyle="dotted", color="gray")
    ax2.axis(ymin=1)
    ax2.get_legend().remove()
   
    plt.show()

# ----------------------------------------------------------------------
if __name__ == "__main__":
        
    print("Plot average of csv files v0.1")
    dir = ""
    if len(sys.argv) != 2:
        print("Usage: plot-stack.py <directory>")
        dir = os.path.dirname(os.path.realpath(__file__))
    
    try:
        if (dir == ""):
            dir = sys.argv[1]
        print("Reading %s" % dir)
        plot_all_csv(dir)
    except Exception as e:
        print(f"Error: {e}")
