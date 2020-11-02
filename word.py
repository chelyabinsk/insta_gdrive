#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A more effecient way to select words.
Sadly, I cannot use pip to install other packages so I have to use RegExp :(
"""

from requests import session
import re
from random import randint, random, shuffle
import json

class Word_picker():
    def __init__(self):
        headers = {
            'Host': 'www.lexico.com',
            'User-Agent':'Mozilla/5.0 (Linux; Android 9; JSN-L21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
            }
        self.site_map_url = 'https://www.lexico.com/sitemaps/list.xml'
        self.definition_url = 'https://www.lexico.com/definition/{}'
        self.s = session()
        self.s.headers = headers
        self.status = 0
        
    def gather_hashtags(self):
        default_hashtags = ['#love','#fashion','#instagood','#style',
                            '#photooftheday','#beautiful','#fitness',
                            '#picoftheday','#follow','#beauty','#like4like',
                            '#art','#ootd','#model','#cute','#followme','#repost',
                            '#instadaily','#happy','#instagram','#makeup',
                            '#girl','#amazing','#photography','#lifestyle',
                            '#me','#smile','#like','#instalike','#life','#fun',
                            '#selfie','#summer','#tbt','#igers','#bestoftheday',
                            '#kilif','#telefon','#aksesuar','#diamond',
                            '#moda','#colorful','#snapchat','#case','#best',
                            '#grils','#good','#apple','#takip','#stylis',
                            '#istanbul','#kapak','#ankara','#akillitefon',
                            '#turkiye','#rabbit','#besiktas','#galatasaray',
                            '#fenerbahce','#airjacket','#kilifsiparis','#kiz',
                            '#siparis']
        shuffle(default_hashtags)
        return default_hashtags[:randint(9, 13)]
        
    def read_backup_words(self):
        # Read the backup file
        with open('misc/data.json','r',encoding='utf8') as f:
            file = json.loads(f.read())
        pos = randint(401, len(file)-1)
        return file[pos]
        
    def find_page_url(self):
        # Get site maps
        r = self.s.get(self.site_map_url)
        matches = re.findall('(<loc>(.*?)<\/loc>)',r.text)
        # Pick a random page
        page_num = randint(0, len(matches)-1)
        return matches[page_num][1]
    
    def find_word_url(self):
        page_url = self.find_page_url()
        r = self.s.get(page_url)
        return re.findall('\"\/definition\/(.*?)\"',r.text)
    
    def clean_text(self,text,text_type='sentence'):
        matches = re.findall('<(.*?)>',text)
        for match in matches:
            text = text.replace('<'+match+'>','')
        if text_type == 'word':
            text = re.sub('[0-9]+','',text)
        return text
    
    def get_word(self):
        try:
            words = self.find_word_url()
        except:
            self.status = 1
        fail_count = 0
        while 1 and self.status == 0:
            if random() < 0.2 and fail_count > 0:
                try:
                    words = self.find_word_url()
                except:
                    self.status = 1
                    break
            
            # Pick random word from the page
            rand_pos = randint(0, len(words)-1)
            url = self.definition_url.format(words[rand_pos])
            # url = 'https://www.lexico.com/definition/stunt'
            
            # Check whether the page contains etymology
            try:
                r = self.s.get(url)
            except:
                self.status = 2
                break
            if r.status_code == 200:
                html  = r.text
            else:
                # Need to read the backup file
                self.status = 3
                break
            
            try:
                self.page_data = self.extract_info(html)
            except:
                self.status = 5
                break
            
            self.page_data['url'] = url
            
            # If empty list, choose new word
            if self.page_data['etym'] == '':
                # print('No Etymology')
                fail_count += 1
                continue
            elif self.page_data['phonetics'] == '':
                fail_count += 1
                continue
            else:
                break
            
            if fail_count > 15:
                # Load words from the file
                self.status = 4
                break
                
        if self.status != 0:
            # Something went wrong so load info from the backup file
            self.page_data = self.read_backup_words()
            pass
        else:
            self.page_data['hashtags'] = self.gather_hashtags()
    
    def gen_random_sentence(self,word,html):
        # Look at currently trending words
        # Pick sentence from trending wors
        trend_words = re.findall('<li>(.*?)trending(.*?)href=\"(.*?)\"(.*?)<\/li>',html)
        urls = []
        for w in trend_words:
            urls.append(w[2])
        # Pick a word at random
        poses = [i for i in range(len(urls))]
        shuffle(poses)
        for pos in poses:
            r = self.s.get('https://www.lexico.com'+urls[pos])
            if r.status_code == 200:
                # Try to extract the word name
                curr_word_list = re.findall('<span class="hw"(.*?)>(.*?)<\/span>',r.text)
                if curr_word_list == []:
                    continue
                else:
                    curr_word = curr_word_list[0][1]
                
                sentence = re.findall('<li class=\"ex\">(.*?)<em>&lsquo;(.*?)&rsquo;<\/em><\/li>',r.text)
                if sentence == []:
                    # generate my own sentence...
                    continue
                else:
                    old_sentence = sentence[0][1]
                    # print(curr_word,word)
                    new_sentence = old_sentence.replace(curr_word,word)
                    # print(old_sentence,new_sentence)
                    return new_sentence
                    break
        
        
        
    def extract_info(self,html):
        out = {'etym':'',
               'word':'',
               'phonetics':'',
               'def':'',
               'word_type':'',
               'usage':'',
               'url':'',
               'hashtags':''
               }
        # Try to extract etymology
        etymologies = re.findall('<section class=\"etymology(.*?)<h3><strong>Origin(.*?)<p>(.*?)<\/p>(.*?)<\/section>',html)
        if etymologies == []:
            return out
        else:
            out['etym'] = self.clean_text(etymologies[0][2])
            
        # Try to extract the word name
        word = re.findall('<span class="hw"(.*?)>(.*?)<\/span>',html)
        if word == []:
            return out
        else:
            out['word'] = self.clean_text(word[0][1],'word')
            
        # Try to extract the phonetics
        phonetics = re.findall('<span class=\"phoneticspelling\">(.*?)<\/span>',html)
        if phonetics == []:
            return out
        else:
            out['phonetics'] = phonetics[0]
            
        # Try to extract the definition
        definition = re.findall('<span class=\"ind\">(.*?)<\/span>',html)
        if definition == []:
            return out
        else:
            out['def'] = definition[0]
        
        # Try to find the word type
        w_type = re.findall('<span class=\"pos\">(.*?)<\/span>',html)
        if definition == []:
            return out
        else:
            out['word_type'] = w_type[0]
            
        # Try to find an example sentence
        # Chances are there is no example.. Will have to generate my own 
        # random sentence!
        sentence = re.findall('<li class=\"ex\">(.*?)<em>&lsquo;(.*?)&rsquo;<\/em><\/li>',html)
        if sentence == []:
            # generate my own sentence...
            out['usage'] = self.gen_random_sentence(out['word'],html)
        else:
            out['usage'] = sentence[0][1]   
        return out

if __name__ == '__main__':
    W = Word_picker()
    W.get_word()
    print(W.page_data)
