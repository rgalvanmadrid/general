### Script that queries ADS using astroquery, and downloads the publisher PDFs using the new ADS API ###

from astroquery import nasa_ads as na
import sys
import os

save_path = "/home/roberto/UNAM/IRyA/pubs/"

# if you don't store your token as an environment variable
# or in a file, give it here
na.ADS.TOKEN = '2ANzysu9pnlgNpqO1qNqiXtj5Us8s0z5LrzQIJAi'
# change the number of rows returned
na.ADS.NROWS = 20
# change the fields that are returned (enter as strings in a list)
#na.ADS.ADS_FIELDS = ['author','title','abstract','pubdate']

# do the query
results = na.ADS.query_simple('Galvan-Madrid, R')  
bibcodes = results['bibcode']
#print(bibcodes)

# Use ADS API to download pdf from publisher 
# change PUB_PDF to EPRINT_PDF to download arXiv versions 
for element in range(len(bibcodes)):
	#print('Downloading '+bibcodes[element])
	bash_command1 = 'token="your-token-here"'
	bash_command2 = 'curl -H "Authorization: Bearer '+na.ADS.TOKEN+'" '+"'https://ui.adsabs.harvard.edu/link_gateway/"+bibcodes[element]+"/PUB_PDF'"+" -L -o "+save_path+"paper_"+str(element)+".pdf"
	print(bash_command1)
	print(bash_command2)
	os.system(bash_command1)
	os.system(bash_command2)
