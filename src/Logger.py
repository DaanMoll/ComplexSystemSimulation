from datetime import datetime
import numpy as np
import os
import csv

class Logger():
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

    def save_position_step(self, positions):
        if not self.has_header:
            self.columns.append("timestep")
            print(f"saving {self.output_path}")
            self.columns.extend([f"agent_{i}_{xy}" for i in range(len(positions)) for xy in ("x", "y") ])
            with open(self.output_path, 'w+', newline ='') as file:
                write = csv.writer(file)
                write.writerows([self.columns])
            self.has_header = True

        row = [self.time]
        for (x,y) in positions:
            row.extend([x,y])

        self.time += 1
        # writing the data into the file
        with open(self.output_path, 'a', newline ='') as file:
            write = csv.writer(file)
            write.writerows([row])