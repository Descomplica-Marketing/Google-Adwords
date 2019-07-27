import os
from googleads import adwords, common

project_root = os.path.abspath(os.path.join(os.path.realpath('__file__'), os.pardir))

adwords_client = adwords.AdWordsClient.LoadFromStorage(path=project_root + '/googleads.yaml')
adwords_client.cache = common.ZeepServiceProxy.NO_CACHE

report_downloader = adwords_client.GetReportDownloader(version='v201809')
