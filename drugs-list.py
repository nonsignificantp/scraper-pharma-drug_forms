import sys
import json
from modules.pharma import *
from datetime import datetime

# Inside do_NOT_git, "url" and "body" variables are declared.
# As a personal preference, I prefer not to disclose what website is being scraped
from do_NOT_git import * 

def scrap(response):
    response_parsed = parse_response(response.text)
    drugs_list      = getTableWhereDrugNamesAre(response_parsed)

    drugs_names = []
    for drug_item in drugs_list.find_all("form"):
        drug_entry = {}
        for drug_input in drug_item.find_all("input"):
            attributes = drug_input.attrs
            drug_entry[attributes["name"]] = attributes["value"]
        drugs_names.append(drug_entry)

    with open('./data/drugs-names.json', 'w') as jsonfile:
        json.dump({
            'datetime': str(datetime.now()),
            'name': 'drugs-names',
            'data': drugs_names
            }, jsonfile)
    
    print("Success!")

if __name__ == "__main__":
    assert "url" in locals(), "URL was not declared!"
    assert "body" in locals(), "body was not declared!"

    try:
        response = send_post(url, body)
    except:
        print("webpage isn't responding")
        sys.exit(1)
    
    assert response.status_code == 200, "Non 200 status"

    scrap(response)