import sys
import json
from os.path import exists
from modules.pharma import *
from datetime import datetime

# Inside do_NOT_git, "partial_url" variable is declared.
# As a personal preference, I prefer not to disclose what website is being scraped
from do_NOT_git import * 

def run():
    drugs_urls = loadData('./data/drugs-urls.json')
    drugs_data = []

    for drug in drugs_urls['data']:
        
        try:
            response = send_get(f"{item_url}{drug['url']}")
        except:
            drugs_data += [{"status":"ERROR", "which":drug['url'], "msg":"no response"}]
            continue
        
        if response.status_code != 200:
            drugs_data += [{"status":"ERROR", "which":drug['url'], "msg":"no response"}]
            continue
        
        try:
            response_parsed = parse_response(response.text)
            drugs_by_form   = getTableWhereDrugFormsAre(response_parsed)
            drugs_data += extractDrugsData(drugs_by_form)
        except:
            drugs_data += [{"status":"ERROR", "which":drug['url'], "msg":"data not scrapable"}]
            continue
    
    with open('./data/drugs-items.json', 'w') as jsonfile:
        json.dump({
            'datetime': str(datetime.now()),
            'name': 'drugs-items',
            'data': drugs_data
            }, jsonfile)

    print('success!')
    return 0

if __name__ == '__main__':
    assert ('./data/drugs-urls.json'), "Needed JSON file, doesn't seem to exist"
    sys.exit(run())