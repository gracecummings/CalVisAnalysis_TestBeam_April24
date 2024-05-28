import csv
import json
import sys, argparse
import pandas as pd
import numpy as np
import uproot
import os, logging

""" run it with this command: python csv_ <scripts> --csvFilePath <csvfilename> --arrayFilePath <npzfilename>"""

def setup_logger(name='calvis'):
    if name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(name)
        logger.info('Logger %s is already defined', name)
    else:
        fmt = logging.Formatter(
            fmt = (
                f'\033[34m[%(name)s:%(levelname)s:%(asctime)s:%(module)s:%(lineno)s {os.uname()[1]}]\033[0m'
                + ' %(message)s'
                ),
            datefmt='%Y-%m-%d %H:%M:%S'
            )
        handler = logging.StreamHandler()
        handler.setFormatter(fmt)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger
logger = setup_logger()

def multi_range(l, *args):
    output = []
    for indices in args:
        output += l[indices[0]:indices[1]]
    return output

def pull_arg(*args, **kwargs):
    """
    Pulls specific arguments out of sys.argv.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(*args, **kwargs)
    args, other_args = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + other_args
    return args


class Scripter:
    """
    to run the code in command line
    """
    def __init__(self):
        self.scripts = {}

    def __call__(self, fn):
        self.scripts[fn.__name__] = fn
        return fn

    def run(self):
        script = pull_arg('script', choices=list(self.scripts.keys())).script
        logger.info('Running %s', script)
        self.scripts[script]()


scripter = Scripter()

@scripter
def make_json():
        """ Function to convert a CSV to JSON """
        data = {}
        with open(csvFilePath, encoding='utf-8') as csvf:
                csvReader = csv.DictReader(csvf)
                for rows in csvReader:
                        # Run number as the primary key
                        key = rows['Run #']
                        data[key] = rows
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                jsonf.write(json.dumps(data, indent=4))

@scripter
def array_struct():
        """ csv file to dict 
            exclude Date, Time, 'Notes', 'Unnamed: 19', 'Unnamed: 20'
        """
        df = pd.read_csv(csvFilePath)[:-1] # avoid the last line
        all_headers = list(df)
        header = multi_range(all_headers, (2, 8), (11, 18))
        # dict of useful info from 
        # the measurement with assigned types
        types_info = {'Run #':int, 'Energy (GeV)':float,
             'Angle (deg)':float,'Bias HV1 (front, Ch 0-3, V))':float,'Bias HV2 (back, Ch 4-7, V)':float,
             'HV1 Current Avg (mA)':float,'Crystal':str,'# of Events':float,
             'Si Telescope Run Number':float,'Run Name':str,'Bad Run':int,
             'Good Data':int,'Good (Telescope + Data)':int}
        saved_info = {}
        forbiden_type_entry = ['-','nan','?','null']
        for h in header:
            per_info=[]
            type_info=types_info[h]
            for d in df[h].to_numpy():
                try:
                    per_info.append(type_info(d))
                except ValueError:
                    per_info.append(0) if d in forbiden_type_entry else per_info.append(type_info(d))
            saved_info[h] = np.array(per_info)
        np.savez(arrayFilePath, **saved_info)

if __name__ == '__main__':
    csvFilePath  = pull_arg('--csvFilePath', type=str,default='').csvFilePath
    jsonFilePath = pull_arg('--jsonFilePath',  type=str,default='').jsonFilePath
    arrayFilePath  = pull_arg('--arrayFilePath',  type=str,default='').arrayFilePath
    scripter.run()
