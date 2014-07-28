import urllib
import argparse
import os
import urllib2

# note that we should only download if we don't have a local copy

def download_file( sourceurl, targetfname ):
  mem_file = ''
  good_read = False
  xbrlfile = None
  if os.path.isfile( targetfname ):
    print('Local copy already exists')
    return True
  else: 
    print('Downloading:', sourceurl)
    try:
      xbrlfile = urllib.urlopen( sourceurl )
      try:
        mem_file = xbrlfile.read()
        good_read = True
      finally:
        xbrlfile.close()
    except urllib2.HTTPError as e:
      print('HTTP Error:', e.code)
    except URLError as e:
      print('URL Error:', e.reason)
    except TimeoutError as e:
      print('Timeout Error:', e.reason)
    except socket.timeout:
      print('Socket Timeout Error')
    if good_read:
      output = open( targetfname, 'wb')
      output.write( mem_file )
      output.close()
    return good_read


def main():
  parser = argparse.ArgumentParser(description='Run the initialdownload')
  parser.add_argument('--func',help='function to be invoked', type='int')
  parser.add_argument('--month', help='month to be retrieved', type='int')
  parser.add_argument('--year', help='year to be retrieved')
  args = parser.parse_args
  SECDownload(args.year, args.month)

if __name__ == "__main__":
  main()
