import sec_download
import process_rss
import feedparser

def download_and_process(year, month):
  good_read, rss_feed = sec_download.sec_download(year, month)
  if good_read:
    feed = feedparser.parse(rss_feed)
    process_rss.process_rss(feed)
    



def main():
  parser = argparse.ArgumentParser(description='Run the initialdownload')
  parser.add_argument('--func',help='function to be invoked')
  parser.add_argument('--month', help='month to be retrieved', type=int)
  parser.add_argument('--year', help='year to be retrieved', type=int)
  args = parser.parse_args()
  download_and_process(args.year, args.month)


if __name__ == "__main__":
  main()    
