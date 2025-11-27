# VERSION: 1.0
# AUTHORS: rmux
# NOTE: Create a linkomanija_config.json file in the same directory with your credentials:
#       {
#           "login": "your_username",
#           "phpsessid": "your_session_id",
#           "track_key": "meowmeow"
#       }
#       - Get 'login' and 'phpsessid' from your browser cookies using a cookie editor extension
#       - Get 'track_key' from your tracker announce URL (the hash part between port and /announce)
#         If your announce URL is: http://tracker.linkomanija.net:numbers/meowmeow/announce
#         Then your track_key is: meowmeow

import re
import os
import tempfile
import json
from html.parser import HTMLParser
import urllib.request
import urllib.parse
from novaprinter import prettyPrinter


class linkomanija(object):
    url = 'https://www.linkomanija.net'
    name = 'LinkoManija'
    supported_categories = {
        'all': 'all',
        'movies': '29',
        'tv': '30',
        'music': '37',
        'games': '45',
        'anime': '38',
        'software': '32'
    }
    
    def __init__(self):
        self.login = None
        self.phpsessid = None
        self.track_key = None
        self._load_config()
    
    def _load_config(self):
        config_paths = [
            os.path.join(os.path.dirname(__file__), 'linkomanija_config.json'),
            os.path.expanduser('~/linkomanija_config.json'),
            os.path.expanduser('~/Documents/linkomanija_config.json'),
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        self.login = config.get('login')
                        self.phpsessid = config.get('phpsessid')
                        self.track_key = config.get('track_key')
                        return
                except:
                    continue
    
    class MyHtmlParser(HTMLParser):
    
        def error(self, message):
            pass
    
        DIV, TABLE, TBODY, TR, TD, A, SPAN, I, B = ('div', 'table', 'tbody', 'tr', 'td', 'a', 'span', 'i', 'b')
    
        def __init__(self, url, cookies, parent):
            HTMLParser.__init__(self)
            self.url = url
            self.cookies = cookies
            self.parent = parent
            self.row = {}
            self.column = 0

            self.foundTable = False
            self.insideRow = False
            self.insideDataCell = False
            self.rowClass = None

            self.shouldParseName = False
            self.shouldGetSize = False
            self.shouldGetSeeds = False
            self.shouldGetLeechs = False

            self.alreadyParseName = False

        def handle_starttag(self, tag, attrs):
            params = dict(attrs)
            
            if tag == self.TABLE and params.get('border') == '1':
                self.foundTable = True
                return

            if tag == self.TR and self.foundTable:
                self.column = 0
                self.insideRow = True
                self.rowClass = params.get('class', '')
                return

            if tag == self.TD and self.insideRow:
                self.column += 1
                self.insideDataCell = True
                cell_class = params.get('class', '')
                
                if 'colhead' in cell_class or 'rowhead' in cell_class:
                    return
                
                if self.column == 2:
                    return
                
            if self.insideDataCell and self.column == 2 and tag == self.A:
                href = params.get('href', '')
                
                if href.startswith('details?') and not self.alreadyParseName:
                    self.shouldParseName = True
                    self.row['desc_link'] = f'{self.url}/{href}'
                    
                    torrent_id_match = re.search(r'details\?(\d+)', href)
                    if torrent_id_match:
                        torrent_id = torrent_id_match.group(1)
                        self.row['torrent_id'] = torrent_id

        def handle_data(self, data):
            if self.shouldParseName:
                torrent_name = data.strip()
                self.row['name'] = torrent_name
                self.shouldParseName = False
                self.alreadyParseName = True
                
                if 'torrent_id' in self.row:
                    torrent_id = self.row['torrent_id']
                    name_encoded = urllib.parse.quote_plus(torrent_name)
                    download_url = f'{self.url}/download.php?id={torrent_id}&name={name_encoded}.torrent'
                    
                    torrent_file = self.parent.download_and_save_with_message(download_url, torrent_id)
                    if torrent_file:
                        self.row['link'] = f'file:///{torrent_file.replace(os.sep, "/")}'
                    else:
                        self.row['link'] = download_url

            if self.insideDataCell and self.column == 6:
                size_text = data.strip()
                if size_text:
                    if 'size' not in self.row:
                        self.row['size'] = size_text
                    else:
                        self.row['size'] += ' ' + size_text

            if self.insideDataCell and self.column == 8:
                if data.strip() and data.strip().isdigit():
                    self.row['seeds'] = data.strip()

            if self.insideDataCell and self.column == 9:
                if data.strip() and data.strip().isdigit():
                    self.row['leech'] = data.strip()

        def handle_endtag(self, tag):
            if tag == self.TD:
                self.insideDataCell = False

            if tag == self.TR and self.insideRow:
                if self.row.get('name') and self.row.get('link'):
                    self.row['engine_url'] = self.url
                    if 'seeds' not in self.row:
                        self.row['seeds'] = '-1'
                    if 'leech' not in self.row:
                        self.row['leech'] = '-1'
                    if 'size' not in self.row:
                        self.row['size'] = '-1'
                    
                    prettyPrinter(self.row)
                
                self.column = 0
                self.row = {}
                self.insideRow = False
                self.alreadyParseName = False
                self.shouldGetSize = False

    def download_and_save_with_message(self, download_url, torrent_id):
        try:
            req = urllib.request.Request(download_url)
            req.add_header('Cookie', f'login={self.login}; PHPSESSID={self.phpsessid}')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            req.add_header('Referer', self.url)
            
            response = urllib.request.urlopen(req)
            torrent_data = response.read()
            
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, f'linkomanija_{torrent_id}.torrent')
            
            with open(file_path, 'wb') as f:
                f.write(torrent_data)
            
            return file_path
            
        except:
            return None

    def retrieve_url(self, url):
        req = urllib.request.Request(url)
        req.add_header('Cookie', f'login={self.login}; PHPSESSID={self.phpsessid}')
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except Exception as e:
            return ""

    def getPageUrl(self, what, cat):
        search_encoded = urllib.parse.quote(what)
        return f'{self.url}/browse.php?search={search_encoded}'

    def search(self, what, cat='all'):
        page_url = self.getPageUrl(what, cat)
        
        try:
            retrievedHtml = self.retrieve_url(page_url)
            
            if retrievedHtml and ('Paieškos rezultatai:' in retrievedHtml or 'colhead' in retrievedHtml):
                parser = self.MyHtmlParser(self.url, None, self)
                parser.feed(retrievedHtml)
                parser.close()
        except Exception as e:
            pass
