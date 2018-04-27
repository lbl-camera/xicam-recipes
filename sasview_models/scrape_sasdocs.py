#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import re
import urllib3
from bs4 import BeautifulSoup
import pandas
import yaml

base = 'http://www.sasview.org/docs/user/'
URL = 'http://www.sasview.org/docs/user/index.html'
http = urllib3.PoolManager()


def parse_model_page(url):
    request = http.request('GET', url)
    soup = BeautifulSoup(request.data, 'html5lib')
    key = soup.h1.get_text()

    table = soup.table
    keys = [item.get_text() for item in table.thead.find_all('th', attrs={'class':'head'})]
    pars = [[item.get_text() for item in row.find_all('td')] for row in table.tbody.find_all('tr')]
    df = pandas.DataFrame(pars, columns=keys)
    return key, df
     

def get_categories(url):
    request = http.request('GET', url)
    soup = BeautifulSoup(request.data, 'html5lib')
    links = soup.find_all('a', attrs={'class':'reference internal'})
    cats = [ link.get('href') for link in links if not 'model' in link.get('href')]
    
    category = {}
    for cat in cats:
        request = http.request('GET', base+cat)
        soup = BeautifulSoup(request.data, 'html5lib')
        key = soup.h1.get_text()
        urls = soup.find_all('a', attrs={'class':'reference internal'})
        models = [base+url.get('href') for url in urls if 'model' in url.get('href')]
        category[key] = models
    return category 


def df2yaml(df):
    class Parameter(yaml.YAMLObject):
        yaml_tag = '!YMLParameter' 
        def __init__(self, series):
            self.name = series['Parameter']
            self.description = series['Description']
            self.units = series['Units']
            self.value = float(series['Default value'])
        def __repr__(self):
            tag = self.__class__.__name__
            return "%s(name=%r, description=%r, units=%r, value=%r)" % (
                tag, self.name, self.description, self.units, self.value)

    params = []
    df = df.iloc[::-1]
    for _, row in df.iterrows():
        params.append({'param': Parameter(row.to_dict())})
    return params

if __name__ == '__main__':
    tree = {}
    category = get_categories(URL)
    for key, values in category.items():
        node = {}
        for v in values:
            model, df = parse_model_page(v)
            m = ' '.join([w.capitalize() for w in model.split('_')])
            node[m] = df2yaml(df)
        tree[key] = node 

    with open('config.yml', 'w') as fp:
        yaml.dump(tree, fp, default_flow_style=False, indent=4)
