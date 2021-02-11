import requests
import json
import os
import hashlib

link = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'

class HashMaker:

    def __init__(self, link):
        self.link = link

    def download_file(self, link):
        link = self.link
        file_name = link.split('/')[-1]
        resp = requests.get(link, allow_redirects=True)
        with open(file_name, 'wb') as file:
            file.write(resp.content)
            return file_name

    def get_data(self, file_name):
        with open(file_name, 'rb') as file:
            data = json.load(file)
            return data

    def create_file_links(self, data):
        self.data = data
        file_name = 'links.txt'

        if os.path.isfile('links.txt') == True:
            os.remove('links.txt')
        else:
            pass
        for item in data:
            country = item['name']['official']
            with open('links.txt', 'a') as file:
                file.write(f'{country} - "https://en.wikipedia.org/wiki/{country}", \n')
        return file_name

    def get_hashsum(self, file_name):
        self.file_name = file_name

        with open(file_name) as f:
            for line in f:
                hash = hashlib.md5(line.encode())
                res = hash.hexdigest()
                yield res


    def main(self, file_name):
        hashsum = self.get_hashsum(self.create_file_links(self.get_data(self.download_file(link))))

        if os.path.isfile('hashsum.txt') == True:
            os.remove('hashsum.txt')
        else:
            pass

        with open(file_name) as f:
            lines = f.readlines()

        for line in lines:

            while line != lines[-1]:
                with open('hashsum.txt', 'a') as f:
                    f.write(f'{next(hashsum)}, \n')
            else:
                raise StopIteration

hashmaker1 = HashMaker(link)

hashmaker1.main('links.txt')






