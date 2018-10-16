import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_post(url, body):
    """Sends a POST request to xxxx webpage, returns server response"""
    return requests.post(url, data=body)

def send_get(url):
    return requests.get(url)

def parse_response(response):
    """Uses bs4 for parsing HTML to a more usable object"""
    return BeautifulSoup(response, 'html.parser')

def getTableWhereDrugNamesAre(parsed_html):
    """Finds the specific place where data of interest is listed"""
    return parsed_html.find("table", {'class':"estandar"})

def loadData(file_path):
    with open(file_path) as jsonfile:
        return json.load(jsonfile)

def getTableWhereDrugFormsAre(response):
    tabla = response.find("table", {'class':"estandarc"})
    return tabla

def clean_string(string):
    return "".join([verify_char(char) for char in list(string.lower())])

def verify_char(char):
    subs = {'á':"a","é":"e","í":"i", "ó":"o", "ú":"u"}
    return subs[char] if char in subs.keys() else char

def clean_price(price):
    return "".join([verify_price(char) for char in list(price)])

def verify_price(char):
     subs = {"$":"", ",":""}
     return subs[char] if char in subs.keys() else char

def extractDrugsData(tabla):
    first_row  = tabla.find("tr", {"class":"lproducto"})
    brand_name = first_row.find("span", {"class":"tproducto"}).text
    lab_name   = first_row.find("span", {"class":"defecto"}).text
    
    second_row = tabla.find("tr", {"class":"sproducto"})
    drug_name  = second_row.find("td", {'class':"textoe"}).find("span", {"class":"defecto"}).text
    drug_class = second_row.find("td", {'class':"textor"}).find("span", {"class":"defecto"}).text
    
    df_data = []
    dosage_forms = tabla.find_all("td", {"class":"dproducto"})
    for dosage_form in dosage_forms:
        presentacion = dosage_form.find("td", {"class":"tddesc"}).text
        price        = dosage_form.find("td", {"class":"tdprecio"}).text
        last_update  = dosage_form.find("td", {"class":"tdfecha"}).text
        messange     = dosage_form.find("td", {"class":"import"})
        messange_text= messange.text if messange != None else ""

        df_data.append({"brand_name": clean_string(brand_name),
                        "brand_company": clean_string(lab_name),
                        "drug_name": clean_string(drug_name), 
                        "drug_class": clean_string(drug_class),
                        "dosage_form": clean_string(presentacion),
                        "price": clean_price(price),
                        "last_update": str(datetime.strptime(last_update, "(%d/%m/%Y)").date()),
                        "messange": clean_string(messange_text),
                        })
    return df_data
