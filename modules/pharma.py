import requests
from bs4 import BeautifulSoup

def send_post(url, body):
    """Sends a POST request to xxxx webpage, returns server response"""
    return requests.post(url, data=body)

def parse_response(response):
    """Uses bs4 for parsing HTML to a more usable object"""
    return BeautifulSoup(response, 'html.parser')

def getTableWhereDrugNamesAre(parsed_html):
    """Finds the specific place where data of interest is listed"""
    return parsed_html.find("table", {'class':"estandar"})

