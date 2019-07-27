import csv
import re

import pandas as pd

from config import report_downloader


def get_report_df(client_ids, report_query):
    output_file = '/tmp/temporary_file.csv'

    for i in range(len(client_ids)):

        with open(output_file, 'w+') as f:

            report_downloader.DownloadReportWithAwql(report_query, 'CSV', f, client_customer_id=client_ids[i],
                                                     skip_report_header=False, skip_column_header=False,
                                                     skip_report_summary=False, include_zero_impressions=True)

        with open(output_file, 'rt') as f:

            tmp_list = list(csv.reader(f))
            df = pd.DataFrame(tmp_list[2:], columns=tmp_list[1])
            df = df[df["Account"] != ' --']

        if i == 0:
            report = df
        else:
            report = pd.concat([report, df], ignore_index=True)

    report.columns = list(
        map(lambda x: re.sub(' +', ' ', re.sub(r'([^\s\w]|_)+', '', x.lower())).replace(' ', '_'), report.columns))

    return report
