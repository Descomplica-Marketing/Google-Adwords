from googleads import adwords

from functions import get_report_df

report_query = (adwords.ReportQueryBuilder()
                .Select('Date', 'AccountDescriptiveName', 'AdNetworkType1', 'AdNetworkType2', 'AveragePosition',
                        'Clicks', 'ConversionRate', 'Conversions', 'Cost', 'Engagements', 'Impressions')
                .From('ACCOUNT_PERFORMANCE_REPORT')
                .Where('Cost').GreaterThan(0)
                .During('YESTERDAY')
                .Build())

# Create a list with your client ids 
client_ids = ()

report = get_report_df(client_ids, report_query)

# CASTING

# int fields
report[['clicks', 'engagements', 'impressions']] = report[['clicks', 'engagements', 'impressions']].astype(int)

# percentage fields
report['conv_rate'] = report['conv_rate'].str[:-1].astype(float)

# monetary fields
report[['cost']] = report[['cost']].astype(float) / 1000000

# float fields
report[['avg_position', 'conversions']] = report[['avg_position', 'conversions']].astype(float)

print(report)
