import urllib
import argparse
import feedparser
import download_file

# note that we should only download if we don't have a local copy
# use the feedparser5.1.3 package to parse the RSS feed
# https://pypi.python.org/pypi/feedparser
# process RSS feed and walk through all the items contained

def process_rss(feed):
  for item in feed.entries:
    print(item["summary"], item["title"], item["published"])
    '''try:
      #Identify ZIP file enclosure, if available
      enclosures = [l for l in item['links'] if l['rel'] == 'enclosure']
      if ( len( enclosures ) > 0 ):
        #ZIP file enclosure exists, so we can just download the ZIP fle
        enclosure = enclosures[0]
        sourceurl = enclosure["href"]
        cik = item["edgar_ciknumber"]
        targetfname = target_dir + cik + '-' + sourceurl.split('/')[-1]
        retry_counter = 3
        while retry_counter > 0:
          good_read = download_file.download_file( sourceurl, targetfname )
          if good_read:
            break
          else:
            print('Retrying:', retry_counter)
            retry_counter -= 1
    finally:
      #code here'''

def main():
  url = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-2012-01.xml'
  d = feedparser.parse(url)
  process_rss(d)


if __name__=="__main__":
  main()
