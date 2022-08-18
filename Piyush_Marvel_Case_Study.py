import requests
import pandas as pd
import hashlib
import time
from pprint import pprint

def get_marvel_dataframe(public_key, hash, number_of_characters, start_string = ""):
    if(number_of_characters > 100):
        raise Exception('Please specify number of characters less than or equal to 100.')
        
    t = time.strftime('%Y%d%m%H%M%S')
    
    if(start_string == ""):
        response = requests.get('https://gateway.marvel.com:443/v1/public/characters?apikey={}&ts={}&hash={}&limit={}'.format(public_key, t, hash, number_of_characters))
    else:
        response = requests.get('https://gateway.marvel.com:443/v1/public/characters?apikey={}&ts={}&nameStartsWith={}&hash={}&limit={}'.format(public_key, t, start_string, hash, number_of_characters))
    
    raw_data = response.json()
    
#     print(raw_data)
    
    character_info = []
    for character in raw_data['data']['results']:
        character_info.append([character['name'], character['comics']['available'], character['events']['available'], 
                               character['series']['available'], character['stories']['available'], character['id']])
        
    marvels_database = pd.DataFrame(character_info, columns = ['name', 'number_of_comics', 'number_of_events',
                                                               'number_of_series', 'number_of_stories', 'character_id'])
    
    return marvels_database

if __name__ == '__main__':
    
    private_key = str(input("Enter Private Key: "))
    public_key = str(input("Enter Public Key: "))
    num_chars = int(input("The number of characters wanted: "))
    start_string = str(input("Enter start string. If none please leave empty. "))

    m = hashlib.md5()
    m.update("{}{}{}".format(time.strftime("%Y%d%m%H%M%S"), private_key, public_key).encode('utf-8'))
    hash = m.hexdigest()
    
    dataset = get_marvel_dataframe(public_key, hash, num_chars)
    print(dataset.to_markdown())