import urllib
import argparse
import os
import urllib2

# Downloading the data - loading the RSS feed
# use the urlopen function from the urllib package
def SECdownload(year, month):
  root = None
  feedFile = None
  feedData = None
  good_read = False
  itemIndex = 0
  edgarFilingsFeed = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-' + \
                      str(year) + '-' + str(month).zfill(2) + '.xml'
  print(edgarFilingsFeed)
  if not os.path.exists( "sec/" + str(year)):
    os.makedirs("sec/" + str(year))
  if not os.path.exists( "sec/" + str(year) + '/' + str(month).zfill(2)):
    os.makedirs("sec/" + str(year) + '/' + str(month).zfill(2) )
  target_dir = "sec/" + str(year) + '/' + str(month).zfill(2) +'/'
  try:
    feedFile = urllib.urlopen( edgarFilingsFeed )
    try:
      feedData = feedFile.read()
      print(feedData)
      good_read = True
    finally:
      feedFile.close()
  except urllib2.HTTPError as e:
    print("HTTP Error:", e.code)



def main():
  parser = argparse.ArgumentParser(description='Run the initialdownload')
  parser.add_argument('--func',help='function to be invoked')
  parser.add_argument('--month', help='month to be retrieved', type=int)
  parser.add_argument('--year', help='year to be retrieved', type=int)
  args = parser.parse_args()
  SECdownload(args.year, args.month)

if __name__ == "__main__":
  main()
