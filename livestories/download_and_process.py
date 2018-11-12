import threading
import urllib.request
from collections import namedtuple
import pandas as pd
import xlrd
from livestories import BASE
from livestories import YEARS

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
    all_res_countries = pd.DataFrame()
    all_res_states = pd.DataFrame()

    for filename in files:
        df = load_data(url + filename)

        value = df['name'].str.split(",", expand=True)

        df['name'] = value[1]

        res = df.groupby(['name', 'year'])['unemployment'].mean().reset_index(name='avg')
        res = pd.DataFrame(res)
        all_res_states = all_res_states.append(res)

        df['name'] = value[0]
        res = df.groupby(['name', 'year'])['unemployment'].mean().reset_index(name='avg')
        res = pd.DataFrame(res)
        all_res_countries = all_res_countries.append(res)

    all_res_states.to_csv('states.csv', sep='|')
    all_res_countries.to_csv('countries.csv', sep='|')


def load_data(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    workbook = xlrd.open_workbook(file_contents=response.read())
    sheet = workbook.sheet_by_index(0)

    data = []

    for index in range(6, sheet.nrows - 4):
        row = sheet.row_values(index)
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
