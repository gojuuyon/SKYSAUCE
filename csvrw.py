import csv
import os
import numpy as np


class CSV:
    # a manage a csv file
    def __init__(self,fname: str, fields: list) -> None:
        if not os.path.exists(fname):# check if file exists
            # if not, create and add fields
            with open(fname, 'w') as csvF:
                # make a writer object
                csvwriter = csv.writer(csvF)
                # write the fields 
                
        # if so do nothing
        