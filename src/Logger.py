from datetime import datetime
import numpy as np
import os
import csv

class Logger():
    """
    Class to log the positions of agents.
    Output is a csv file with x,y positions for all agents.
    """
    
    def __init__(self, output_dir, debug=False, filename=None):
        if filename != None:
            self.filename = filename
        else:
            self.filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        if not self.filename.endswith(".csv"):
            self.filename += ".csv"
        self.output_dir = output_dir
        self.output_path = os.path.join(self.output_dir, self.filename)
        self.debug = debug
        self.has_header = False
        self.columns = []
        self.time = 0

    def save_position_step(self, positions, orig_distances):
        if not self.has_header:
            self.columns.append("timestep")
            print(f"saving {self.output_path}")
            
            self.columns.extend([f"gate{i}_{xy}" for i in range(2) for xy in ("x", "y", "orig_distance") ])
            self.columns.extend([f"agent_{i}_{xy}" for i in range(len(positions) - 2) for xy in ("x", "y", "orig_distance") ])
            
            with open(self.output_path, 'w+', newline ='') as f:
                write = csv.writer(f)
                write.writerows([self.columns])
            self.has_header = True

        row = [self.time]
        for i in range(len(positions)):
            row.extend([positions[i][0],positions[i][1], orig_distances[i]])

        self.time += 1

        with open(self.output_path, 'a', newline ='') as f:
            write = csv.writer(f)
            write.writerows([row])

if __name__ == '__main__':
    print("Running this file does not do anything.")   