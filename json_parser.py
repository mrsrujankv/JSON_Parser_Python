import requests
import json
import io
import ftplib


url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
filename_to_save = 'download.json'
r = requests.get(url,auth=('user', 'pass'))
with open(filename_to_save, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
results = []
with open('download.json', 'r') as f:
    content = json.loads(f.read())
    results.append('\t'.join(['id', 'title', 'description', 'product_type',
                             'link', 'image_link', 'brand', 'sale_price',
                             'availability', 'condition', 'price']))
    for element in content['offers']:
        results.append('\t'.join([element.get('offerId', ''), element.get('title', ''),
                                  element.get('offerDescription', ''), ",".join(element.get('categories', [])),
                                  element.get('offerURL', ''), element.get('imageURL', ''),
                                  ",".join(element.get('brandNames', [])), str(element.get('value', '')),
                                  element.get('expirationDate', ''),
                                  element.get('_condition', ''), element.get('_price', '')
                                  ]))
# print '\n'.join(results)

with io.open('test_converted.tsv', 'w', encoding='utf8') as f:
    f.write('\n'.join(results))

session = ftplib.FTP('server.address.com','USERNAME','PASSWORD')
file = open('test_converted.tsv','rb')                  # file to send
session.storbinary('target_extract.tsv', file)          # send the file
file.close()                                            # close file and FTP
session.quit()
