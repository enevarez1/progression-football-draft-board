import csv

from src.report.model import Evaluation, Exercise, Player

def retrieve_csv(file_path):
    with open(file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        return csvFile
