#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example downloads a criteria performance report as a string with AWQL.

To get report fields, run get_report_fields.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

from googleads import adwords


# Specify where to download the file here.
PATH = '/tmp/report_download.csv'


def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('CampaignId', 'AdGroupId', 'Id', 'Criteria',
                          'CriteriaType', 'FinalUrls', 'Impressions', 'Clicks',
                          'Cost')
                  .From('CRITERIA_PERFORMANCE_REPORT')
                  .Where('Status').In('ENABLED', 'PAUSED')
                  .During('LAST_7_DAYS')
                  .Build())

  print((report_downloader.DownloadReportAsStringWithAwql(
        report_query, 'CSV', skip_report_header=False, skip_column_header=False,
        skip_report_summary=False, include_zero_impressions=True)))


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client)
