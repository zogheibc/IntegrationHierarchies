##SCRIPT FOR WEBSCRAPING (FOR CANADIAN PUBLIC SECTOR INTEGRATION PROJECT)
##Author: Ciara Zogheib

##import packages
import praw
import pandas as pd
import numpy as np
import nltk 
nltk.download('punkt')
nltk.download('stopwords')
#from nltk import punkt
from nltk import word_tokenize
import requests ##to get website html
from bs4 import BeautifulSoup ##to work with the html text


######FIRST WE EXPLORE MANDATE LETTERS

##make list of names of webpages with mandate letters to scrape 
sites = ["https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-intergovernmental-affairs-infrastructure-and-communities",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-agriculture-and-agri-food-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-innovation-science-and-industry-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-natural-resources-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-fisheries-oceans-and-canadian-coast-guard-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-environment-and-climate-change-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-public-safety-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-tourism-and-associate-minister-finance-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/deputy-prime-minister-and-minister-finance-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-veterans-affairs-and-associate-minister-national-defence",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-mental-health-and-addictions-and-associate-minister-health",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-health-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-foreign-affairs-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-national-revenue-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-international-development-and-minister-responsible-pacific",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-employment-workforce-development-and-disability-inclusion",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-indigenous-services-and-minister-responsible-federal-economic",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-families-children-and-social-development-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-housing-and-diversity-and-inclusion-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-labour-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-official-languages-and-minister-responsible-atlantic-canada",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-canadian-heritage-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/president-kings-privy-council-canada-and-minister-emergency-preparedness",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-international-trade-export-promotion-small-business-and",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-public-services-and-procurement-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-justice-and-attorney-general-canada-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-national-defence-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/president-treasury-board-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-crown-indigenous-relations-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-northern-affairs-minister-responsible-prairies-economic",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-transport-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-immigration-refugees-and-citizenship-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/leader-government-house-commons-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-rural-economic-development-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-women-and-gender-equality-and-youth-mandate-letter",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-responsible-federal-economic-development-agency-southern",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-sport-and-minister-responsible-economic-development-agency",
         "https://pm.gc.ca/en/mandate-letters/2021/12/16/minister-seniors-mandate-letter"
    ] 
pages = [] 
for site in sites:
    ##get html from website
    page = requests.get(site)
    ##now make a beautifulsoup instance (an object) of our parsed html content
    soup = BeautifulSoup(page.content, 'html.parser')
    ##get all the text
    text = soup.find_all(text=True)
    ##clear out some of the unwanted stuff from the text
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script'
    ]
    ##now add all the text leftover into our output string
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    ##remove newlines from our output text
    output = output.replace('\n',"")
    ##flag as mandate letters
    kind = "Mandate Letter"
    ##now add to our list
    pages.append([site, output, kind]) ##making nested lists

##convert our list of lists to a pandas dataframe
pages = pd.DataFrame(pages,columns=['site','contents', 'kind'])
pages.head(5)
 
##make lists to hold frequency counts for words of interest
integratecount=[]
integrationcount=[]
integratedcount=[]
integratingcount=[]

##now clean up the text contents from each site
for row in pages.contents:
    ##tokenize our string
    site_text_tokens = word_tokenize(row)
    ##turn our string into an nltk text
    site_text = nltk.Text(site_text_tokens)
    ##get list of words only (not punctuation)
    site_words = [w for w in site_text if w.isalpha()]
    ##make lowercase
    site_words = [w.lower() for w in site_words]
    #print(site_words)
    ##load stopwords
    stopwords = nltk.corpus.stopwords.words("english")
    ##remove stopwords from our words list
    site_words = [w for w in site_words if w not in stopwords]
    
    ##get frequency distribution of words
    fd = nltk.FreqDist(site_words)
    ##tabulate data
    fd.tabulate()

    ##search for a particular word to output how many times it appears
    integrate = fd["integrate"]
    integration = fd["integration"]
    integrated = fd["integrated"]
    integrating = fd["integrating"]

    ##add to our lists
    integratecount.append(integrate)
    integrationcount.append(integration)
    integratedcount.append(integrated)
    integratingcount.append(integrating)
    
##add our term frequency counts to our dataframe
pages['integratecount'] = integratecount
pages['integrationcount'] = integrationcount
pages['integratedcount'] = integratedcount
pages['integratingcount'] = integratingcount
pages.head(5)


######NOW WE EXPLORE DEPARTMENTAL PLANS

##make list of names of webpages with dept plans to scrape 
sitesDP = ["https://agriculture.canada.ca/en/department/transparency/departmental-plan/2022-2023",
         "https://ised-isde.canada.ca/site/planning-performance-reporting/en/departmental-plans/2022-23-departmental-plan",
         "https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/departmental-plan-formerly-reports-on-plans-and-priorities/departmental-plan-2022-23/24047",
         "https://www.dfo-mpo.gc.ca/rpp/2022-23/dp-eng.html",
         "https://www.canada.ca/en/environment-climate-change/corporate/transparency/priorities-management/departmental-plans/2022-2023.html",
         "https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/dprtmntl-pln-2022-23/index-en.aspx",
         "https://www.canada.ca/en/department-finance/corporate/transparency/plans-performance/departmental-plans/2022-2023/report.html",
         "https://www.veterans.gc.ca/eng/about-vac/publications-reports/reports/departmental-plan/2022-2023",
         "https://www.canada.ca/en/department-national-defence/corporate/reports-publications/departmental-plans/departmental-plan-2022-23.html",
         "https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/report-plans-priorities/2022-2023-report-plans-priorities.html",
         "https://www.international.gc.ca/transparency-transparence/departmental-plan-ministeriel/2022-2023.aspx?lang=eng",
         "https://www.canada.ca/en/revenue-agency/corporate/about-canada-revenue-agency-cra/departmental-plan/2022-23-cra-departmental-plan.html",
         "https://www.canada.ca/en/employment-social-development/corporate/reports/departmental-plan/2022-2023.html",
         "https://www.sac-isc.gc.ca/eng/1642087807510/1642087838500",
         #"https://www.clo-ocol.gc.ca/en/transparency/departmental-plans/2022-23-departmental-plan",
         "https://www.canada.ca/en/canadian-heritage/corporate/publications/plans-reports/departmental-plan-2022-2023.html",
         "https://www.canada.ca/en/privy-council/corporate/transparency/planned-spending/departmental-plans/2022-2023.html",
         "https://www.tpsgc-pwgsc.gc.ca/rapports-reports/pm-dp/2022-2023/index-eng.html",
         "https://www.justice.gc.ca/eng/rp-pr/cp-pm/rpp/2022_2023/index.html",
         "https://www.canada.ca/en/treasury-board-secretariat/corporate/reports/treasury-board-canada-secretariat-2022-23-departmental-plan.html",
         "https://www.rcaanc-cirnac.gc.ca/eng/1643042950445/1643042973736",
         "https://tc.canada.ca/en/corporate-services/transparency/corporate-management-reporting/departmental-plans/transport-canada-2022-2023-departmental-plan",
         "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/departmental-plan-2022-2023/departmental-plan.html",
         "https://women-gender-equality.canada.ca/en/transparency/departmental-plans/2022-2023.html",
         "https://ced.canada.ca/en/departmental-publications/2022-23-departmental-plan/",
         "https://www.canada.ca/en/pacific-economic-development/corporate/transparency/departmental-plans/2022-2023-departmental-plan.html",
         "https://ised-isde.canada.ca/site/feddev-ontario/en/transparency/departmental-plan/2022-23-departmental-plan",
         "https://www.canada.ca/en/prairies-economic-development/corporate/transparency/departmental-plans/dp-2022-2023.html",
         "https://www.cannor.gc.ca/eng/1644248160701/1644248188049",
         "https://www.canada.ca/en/atlantic-canada-opportunities/corporate/transparency/2022-23-departmental-plan.html",
         "https://www.ic.gc.ca/eic/site/FedNor-FedNor.nsf/eng/h_fn04628.html"
    ] 
pagesDP = [] 
for site in sitesDP:
    ##get html from website
    page = requests.get(site)
    ##now make a beautifulsoup instance (an object) of our parsed html content
    soup = BeautifulSoup(page.content, 'html.parser')
    ##get all the text
    text = soup.find_all(text=True)
    ##clear out some of the unwanted stuff from the text
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script'
    ]
    ##now add all the text leftover into our output string
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    ##remove newlines from our output text
    output = output.replace('\n',"")
    ##flag as departmental plans
    kind = "Departmental Plan"
    ##now add to our list
    pagesDP.append([site, output, kind]) ##making nested lists

##convert our list of lists to a pandas dataframe
pagesDP = pd.DataFrame(pagesDP,columns=['site','contents', 'kind'])
pagesDP.head(5)

    
##make lists to hold frequency counts for words of interest
integratecountDP=[]
integrationcountDP=[]
integratedcountDP=[]
integratingcountDP=[]

##now try to clean up the text contents from each site
for row in pagesDP.contents:
    ##tokenize our string
    site_text_tokens = word_tokenize(row)
    ##turn our string into an nltk text
    site_text = nltk.Text(site_text_tokens)
    ##get list of words only (not punctuation)
    site_words = [w for w in site_text if w.isalpha()]
    ##make lowercase
    site_words = [w.lower() for w in site_words]
    #print(site_words)
    ##load stopwords
    stopwords = nltk.corpus.stopwords.words("english")
    ##remove stopwords from our words list
    site_words = [w for w in site_words if w not in stopwords]

    
    ##get frequency distribution of words
    fdDP = nltk.FreqDist(site_words)
    ##tabulate data
    fdDP.tabulate()

    ##search for a particular word to output how many times it appears
    integrateDP = fdDP["integrate"]
    integrationDP = fdDP["integration"]
    integratedDP = fdDP["integrated"]
    integratingDP = fdDP["integrating"]

    ##add to our lists
    integratecountDP.append(integrateDP)
    integrationcountDP.append(integrationDP)
    integratedcountDP.append(integratedDP)
    integratingcountDP.append(integratingDP)
    
##add our term frequency counts to our dataframe
pagesDP['integratecount'] = integratecountDP
pagesDP['integrationcount'] = integrationcountDP
pagesDP['integratedcount'] = integratedcountDP
pagesDP['integratingcount'] = integratingcountDP
pagesDP.head(5)

####NOW WE MERGE OUR MANDATE LETTERS AND DEPARTMENTAL PLANS DATAFRAMES INTO ONE
pagestotal = pages.append(pagesDP, ignore_index=True)

##export to excel
pagestotal.to_excel('IH_TermCounts.xlsx', index=False)



