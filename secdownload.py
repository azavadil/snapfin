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
    feedFile = urlopen( edgarFilingsFeed )
    try:
      feedData = feedFile.read()
      good_read = True
    finally:
      feedFile.close()
  except HTTPError as e:
    print("HTTP Error:", e.code)

# use the feedparser5.1.3 package to parse the RSS feed
# https://pypi.python.org/pypi/feedparser
# process RSS feed and walk through all the items contained

def processRss(feed):
  for item in feed.entries:
    print(item["summary"], item["title"], item["published"])
    try:
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
          good_read = dowloadfile( sourceurl, targetfname )
          if good_read:
            break
          else:
            print('Retrying:', retry_counter)
            retry_counter -= 1

# note that we should only download if we don't have a local copy

def downloadFile( sourceurl, targetfname ):
  mem_file = ''
  good_read = False
  xbrlfile = None
  if os.path.isfile( targetfname ):
    print('Local copy already exists')
    return True
  else: 
    print('Downloading:', sourceurl)]
    try:
      xbrlfile = urlopen( sourceurl )
      try:
        mem_file = xbrlfile.read()
        good_read = True
      finally:
        xbrlfile.close()
    except HTTPError as e:
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

# for 2005-2007 most filings do not yet contain a zip file enclosure
# in those cases extra work is required to download all the individual
# xbrl files and zip them up locally

# manually download all XBRL files and ZIP them ourselvs


linkname = item['link'].split('/')[-1]
linkbase = os.path.splittext(linkname)[0]
cik = item['edgar_ciknumber']
zipfname = target_dir + cik + '-'+linkbase + '-xbrl.zip'
if os.path.isfile( zipfname )
  print('Local copy already exists')
else:
  edgarNamespance = {'edgar': 'http://www.sec.gov/Archives/edgar'}
  currentItem = list(root.iter('item'))[itemIndex]
  xbrlFiling = currentItem.find('edgar:xbrlFiling', edgarNamespace)
  xbrlFilesItem = xbrlFiling.find('edgar:xbrlFiles', edgarNamespace)
  xbrlFiles = xbrlFilesItem.findall('edgar:xbrlFile', edgarNamespace)
  if not os.path.exists( target_dir + 'temp')
    os.makedirs( target_dir + 'temp')
  zf = zipfile.ZipFile( zipfname, 'w')
  try:
    for xf in xbrlFiles:
      xfurl = xf.get('{http://www.sec.gov/Archives/edgar}url')
      if xfurl.endswith( ('.xml', '.xsd')):
        targetfname = target_idr + 'temp/' + xfurl.split('/')[-1]
        retry_counter = 3
        while retry_counter > 0:
          good_read = downloadfile( xfurl, targetfname )
          if good_read:
            break
          else:
            print('Retrying: ', retry_counter)
            retry_counter -= 1
        zf.write( targetfname, xfurl.split('/')[-1], zipfile.ZIP_DEFLATED)
        os.remove( targetfname )
  finally:
    zf.close()
    os.rmdir( target_dir+'temp')


def lookup_cik(ticker, name=None):
  # Given a ticker symbol, retrieves the CIK
  good_read = False
  ticker = ticker.strip().upper()
  url = 'http://www.sec.gov/cgi-bin/browse-edgar/action-getcompny&CIK=(cik)&count=10&output=xmp'.format(cik=ticker)

  try:
    xmlFile = urlopen( url )
    try:
      xmlData = xmlFile.read()
      good_read = True
    finally:
      xmlFile.close()
  except HTTPError as e:
    print('HTTP Error', e.code)
  except URLError as e:
    print('Url Error', e.reason)
  except TimeoutError as e:
    print('Timeout Error', e.reason)
  except socket.timeout:
    print('Socket Timeout Error')
  if not good_read:
    print('Unable to lookup CIK for ticker', ticker)
    return
  try:
    root = ET.fromstring(xmlData)
  except ET.ParseError as perr:
    print('XML Parser error:', perr)

  try:
    cikElement - list(root.iter('CIK'))[0]
    return int(cikElement.text)
  except StopIteration:
    pass

## result = call(['raptorxmlxbrl', 'xbrl','--listfile', joblist])


def appendjoblist( year, month, cik=None):
  target_dir = 'sec/' + str(year) + '/' + str(month).zfill(2) + '/'
  cikPattern = None
  if not cik==None:
    cikStr = list(map(str, cik))
    cikPattern = tuple(cs.zfill(10) for cs in cikStr)
  try:
    for filename in os.listdir( target_dir ):
      add_file = False
      if os.path.splittext(filename)[1] == '.zip':
        if cik == None:
          add_file = True
        else:
          if filename.startswith( cikPattern ):
            add_file = True
        if add_file:
          zipname = target_dir + filename
          joblist.append( zipname )
  except FileNotFoundError as fe:
    print('Error: no SEC filings found in directory', target_dir)


## result = call(['raptorxmlxbrl', 'xbrl', '--script=' + script, '--listfile', joblist])

def on_xbrl_valid( job, instance):
  # code here



def summaryStatistics():
  currentRatio = 0
  print('\t\tCurrent Ratio = Current Assets / Current Liabilities: ')
  currentAssetsFacts = factFinder( instance, fasb_ns, 'AssetsCurrent')
  currentLiabilitiesFacts = factFinder( instance, fasb_ns, 'LiabilitiesCurrent')
  currentAssets = printFacts( currentAssetsFacts, 3, docEndData )
  currentLiabilities = printFacts( currentLiabilitiesFacts, 3, docEndDate )
  if not currentLiabilites == 0:
    currentRatio = currentAssets / currentLiabities
  print( 3 * '\t', 'Current Ratio = '.ljust(100-3*8), '{0:.2f)'.format( currentRatio))

def quickRatio():
  quickRatio = 0
  print( '\t\tQuick Ratio = (Cash + Short-Term Marketable Securities + Accounts Receivable ) / Current Liabilities: ')
  cashFacts = factFinder( instance, fasb_ns, 'Cash')
  if len(cashFacts) == 0:
    cashFacts = factFinder( instance, fasb_ns, "CashAndCashEquivalentsAtCarryingValue")
  if len(cashFacts) == 0:
    cashFacts = factFinder( instance, fasb_ns, "CashCashEquivalentsAndShortTermInvestments")
  marketableSecuritiesFacts = factFinder( instance, fasb_ns, 'MarketableSecuritiesCurrent')
  if len(marketableSecuritiesFacts) == 0:
    marketableSecuritiesFacts = factFinder( instance, fasb_ns, 'AvailableForSaleSecuritiesCurrent')
  accountsReceivableFacts = factFinder( instance, fasb_ns, 'AccountsReceivableNetCurrent')
  currentLiabilitiesFacts = factFinder( instance, fasb_ns, 'LiabiltiesCurrent')
  cash = printFacts( cashFacts, 3, docEndDate)
  marketableSecurities = printFacts( marketableSecuritiesFacts, 3, docEndDate)
  accountsReceivable = printFacts( accoutnsReceivableFacts, 3, docEndDate)
  currentLiabilties = printFacts( currentLiabilitiesFacts, 3, docEndDate)
  if not currentLiabilities==0:
    quickRatio = (cash + marketableSecurities + accountsReceivable) / currentLiabilities
  print( 3 * '\t', 'Quick Ratio = '.ljust(100-3*8),'{0:.2f)'.format( quickRatio))