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

"""This example adds an HTML5 ad to a given AdGroup.

To get ad_group_id, run get_ad_groups.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


from urllib.request import urlopen

from googleads import adwords


AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'


def main(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_ad_service = client.GetService('AdGroupAdService', version='v201809')

  # Create HTML5 media.
  html5_zip = GetHTML5ZipFromUrl('https://goo.gl/9Y7qI2')
  # Create a media bundle containing the zip file with all the HTML5 components.
  media_bundle = {
      'xsi_type': 'MediaBundle',
      'data': html5_zip,
      'entryPoint': 'carousel/index.html',
      'type': 'MEDIA_BUNDLE'
  }

  ad_data = {
      'uniqueName': 'adData',
      'fields': [
          {
              'name': 'Custom_layout',
              'fieldMedia': media_bundle,
              'type': 'MEDIA_BUNDLE'
          },
          {
              'name': 'layout',
              'fieldText': 'Custom',
              'type': 'ENUM'
          }
      ]
  }

  html5_ad = {
      'xsi_type': 'TemplateAd',
      'name': 'Ad for HTML5',
      'templateId': 419,
      'finalUrls': ['https://www.google.com'],
      'displayUrl': 'www.google.com?tip=ENTER_YOUR_OWN_FINAL_AND_DISPLAY_URLS',
      'dimensions': {
          'width': '300',
          'height': '250'
      },
      'templateElements': [ad_data]
  }

  ad_group_ad = {
      'adGroupId': ad_group_id,
      'ad': html5_ad,
      'status': 'PAUSED'
  }

  operations = [
      {
          'operator': 'ADD',
          'operand': ad_group_ad
      }
  ]
  ads = ad_group_ad_service.mutate(operations)

  # Display results.
  for ad in ads['value']:
    print(('New HTML5 Ad with id "%s" and of display url "%s" was added.'
          % (ad['ad']['id'], ad['ad']['displayUrl'])))


def GetHTML5ZipFromUrl(url):
  """Retrieve zip file from the given URL."""
  response = urlopen(url)
  # Note: The utf-8 decode is for 2to3 Python 3 compatibility.
  return response.read().decode('utf-8')


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, AD_GROUP_ID)
