import json
from os.path import exists
from modules.pharma import *
from datetime import datetime

# Inside do_NOT_git, "url" and "body" variables are declared.
# As a personal preference, I prefer not to disclose what website is being scraped
from do_NOT_git import * 

def scrapError(body, msg):
    print(f'ERROR: {msg}')
    print(f'ITEMS: {body}')
    body['error'] = msg
    return body

if __name__ == '__main__':
    assert exists('./data/drugs-names.json'), "Needed JSON file, doesn't seem to exist"
    with open('./data/drugs-names.json') as jsonfile:
        drug_names = json.load(jsonfile)
    
    drugs = []
    for body in drug_names['data']:
        assert "url" in locals(), "URL was not declared!"
        try:
            response = send_post(url, body)
        except:
            drugs.append(scrapError(body, "webpage didn't responded"))
            continue

        if response.status_code != 200:
            drugs.append(scrapError(body, 'status not 200'))
            continue
        
        response_parsed = parse_response(response.text)
        drugs_by_lab    = getTableWhereDrugNamesAre(response_parsed)
        
        if not any(drugs_by_lab.find_all("form")):
            drugs.append(scrapError(body, 'Empty list'))
            continue

        for drug in drugs_by_lab.find_all("form"):
            drug_add = {}
            if drug.attrs["action"] != "srv":
                drug_add['drug_name'] = body['patron']
                drug_add['url'] = drug.attrs["action"]
                for inputs in drug.find_all("input"):
                    attributes = inputs.attrs
                    drug_add[attributes["name"]] = attributes["value"]
                drugs.append(drug_add)
    
    with open('./data/drugs-urls.json', 'w') as jsonfile:
        json.dump({
            'datetime': str(datetime.now()),
            'name': 'drugs-urls',
            'data': drugs
            }, jsonfile)
    
    print("Success!")