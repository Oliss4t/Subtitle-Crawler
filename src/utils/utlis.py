import click
import openpyxl
from pathlib import Path
import csv
import os

# def print_method_result_to_user(_result: [], _movies_found: [] = None ):
#     """
#     prints the colored result from methods to the command line.
#     """
#     click.secho(_result["Success"], fg="green", bold=True)if _result["Success"] else click.secho(_result["Error"], fg="red", bold=True)
#     if _movies_found is not None:
#         for _m in _movies_found:
#             click.secho(_m['MovieReleaseName'])

def read_from_xlsx_file(_filename: str, _directory: str) -> {}:
    """
    reads and converts data from an xlsx file to a dictionary
    :param _filename: filename of the xlsx file containing the information movie name, season, episode
    :return: dictionary of movies and series
    """
    _xlsx_file = Path(_directory, f"{_filename}.xlsx")
    _wb_obj = openpyxl.load_workbook(_xlsx_file)
    _sheet = _wb_obj.active
    _data = []

    for _i, _row in enumerate(_sheet.iter_rows(values_only=True)):
        if _i != 0:
            _data.append({"query": _row[0], "season": _row[1] if _row[1] else "", "episode": _row[2] if _row[2] else ""})
    return _data


def read_ids_from_csv(_filename: str, _directory: str) -> []:
    csv_file_path = Path(_directory, f"{_filename}.csv")
    ids = []
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            ids.append(*row)
    return ids