import json
import psycopg2
import xml.etree.ElementTree as ET

import pandas.io.sql as psql
import numpy as np

from pandas import *
from xlwt import easyxf, Borders, Workbook, Pattern, Style

def data_connection(conn_string):
    conn = psycopg2.connect(conn_string)
    return conn

def data_frame(query, connection):
    df = psql.frame_query(query, con=connection)
    return df

def generate_report(data_frame, format='crosstab', output='html'):
    if output=='html':
        return data_frame.to_html()

def parse_report(tryp_file):
    tryp_reports = []
    tree = ET.parse(tryp_file)
    root = tree.getroot()
    reports = root.find("reports")
    for report in reports:
        ds_name = report.find("dataset").text
        dataset = root.find(".//datasets/dataset/[@name='%s']" % ds_name)
        query = dataset.find('query').text
        conn_name =  dataset.find('connection').text
        connection = root.find(".//connections/connection/[@name='%s']" % conn_name)
        host = connection.find("host").text
        port = connection.find("port").text
        database = connection.find("database").text
        user = connection.find("user").text
        password = connection.find("password").text
        conn_str = "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (host, port, database, user, password)
        tryp_reports.append({"query": query, "conn_str": conn_str})
    return tryp_reports
    


if __name__ == '__main__':
    reports = parse_report("daily_sales.tryp")
    for report in reports:
        conn = data_connection(report["conn_str"])
        df = data_frame(report["query"], conn)
        df_raw = pivot_table(df, rows=['region','area','distributor','salesrep_name'], aggfunc={'net_sales':np.sum,'sales_order_id_count': np.sum})
        #open('test.html', 'w').write(generate_report(df_raw, 'html'))
        #df_region = pivot_table(df, rows=['region'], aggfunc={'net_sales':np.sum,'sales_order_id_count': np.sum})
        #open('test1.html', 'w').write(generate_report(df_region, 'html'))

        wb = Workbook()
        ws = wb.add_sheet('SHIT')
        for i, row in enumerate(df_raw.to_records()):
            for j, col in enumerate(row):
                ws.write(i, j, col)
        wb.save('SHIT.xls')
