from googleads import adwords

from functions import get_report_df

report_query = (adwords.ReportQueryBuilder()
                .Select('Date', 'AccountDescriptiveName', 'AdNetworkType1', 'AdNetworkType2', 'AveragePosition',
                        'Clicks', 'ConversionRate', 'Conversions', 'Cost', 'Engagements', 'Impressions')
                .From('ACCOUNT_PERFORMANCE_REPORT')
                .Where('Cost').GreaterThan(0)
                .During('YESTERDAY')
                .Build())

client_ids = (
    '544-463-1325', '581-972-9913', '961-537-2652', '261-376-2623', '645-101-8338', '626-926-9193', '875-081-6111',
    '216-595-8325', '433-261-3982')

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
