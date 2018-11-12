import os
import threading
from collections import namedtuple
from pprint import pprint

from livestories import BASE
from livestories import YEARS

import pandas as pd

import urllib.request
import xlrd

UnemploymentRecord = namedtuple('UnemploymentRecord', ('laus_code',
                                                       'state_fips_code',
                                                       'country_fips_code',
                                                       'name',
                                                       'year',
                                                       'labor_force',
                                                       'employed',
                                                       'unemployment',
                                                       'unemployment_rate'))


def main():
    values = YEARS.split(",")

    files = []

    for item in values:
        current = "laucnty" + str(item) + ".xlsx"
        files.append(current)


    threading.Thread(target=download_files, args=(BASE, files)).start()


def download_files(url, files):
    for filename in files:
        pd = load_data(url + filename)

        value = pd['name'].str.split(",", expand=True)

        pd['name'] = value[1]

        df = pd.groupby(['name', 'year'])['unemployment'].mean()
        df.to_csv('out1.csv', sep='|')

        pd['name'] = value[0]
        df = pd.groupby(['name', 'year'])['unemployment'].mean()
        df.to_csv('out2.csv', sep='|')


def load_data(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    workbook = xlrd.open_workbook(file_contents=response.read())
    sheet = workbook.sheet_by_index(0)

    data = []

    for i in range(6, sheet.nrows - 4):
        row = sheet.row_values(i)
        record = build_unemployment_tuple(row)
        data.append(record)

    return pd.DataFrame(data, columns=UnemploymentRecord._fields)


def build_unemployment_tuple(row):
    record = UnemploymentRecord(
        laus_code=row[0],
        state_fips_code=row[1],
        country_fips_code=row[2],
        name=row[3],
        year=int(row[4]),
        labor_force=int(row[6]) if row[6] != 'N.A.' else 0,
        employed=int(row[7]) if row[7] != 'N.A.' else 0,
        unemployment=int(row[8]) if row[8] != 'N.A.' else 0,
        unemployment_rate=float(row[9]) if row[9] != 'N.A.' else 0.)

    return record


if __name__ == '__main__':
    main()
