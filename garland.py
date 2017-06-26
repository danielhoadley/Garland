## (c) 2017. Daniel Hoadley
## Tokenize text files into sentences and writes the output to MongoDB as key(sentence)/value(source filename) pairs.
## Start mongodb instance first with ./mongod

import json
from pymongo import MongoClient
import nltk.data
import codecs
import os
from nltk.tokenize import sent_tokenize

## Run clean.py before executing this script.

## Connect to MongoDB instance and create new database/collection

client = MongoClient('localhost', 27017)
db = client['test-database']
collection = db['sentences']

# Create empty dictionary object

d = {}

# Read the source files

directory = '/Users/danielhoadley/Documents/Development/Python/regex'

for filename in os.listdir(directory):
    
    if filename.endswith('.cln'):
        
        source = codecs.open(filename, 'r', 'utf-8')
        content = source.read()
        name = source.name

# Tokenise the source file into sentences

        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = sent_tokenize(content)
        print content
        print sents
        
# Deduplicate the list of sentences to remove instances where a sentence appears multiple times in the same case
        deduped_sents = list(set(sents))

# Clean the list because mongo doesn't like fullpoints in the key

        clean_sents = map(lambda each:each.strip(u'.'),deduped_sents)
        fresh_sents = map(lambda each:each.strip(),clean_sents)
        cleaned = [word.replace(':', '.') for word in fresh_sents]

        # Populate the empty dictionary with the sentences as keys and the filename as a value

        for i in cleaned:
            d.setdefault(i, []).append(name)

# Remove keys that are less than 50 characters in length

for k in d.keys():
    if len(k) <= 50:
        del d[k]

# Iterate over the dictionary and write each key/value pair to MongoDB as an object

for key, value in d.iteritems():
    sentence_id = db.sentences.insert_one({'sentence': key, 'files': value})

# Dump the output to the console so I can eyeball it

print json.dumps(d.items(), sort_keys=True, indent=4) # output the dictionary as prettified json

print '\nSentences extracted and written to MongoDB!\n'

# db.getCollection('sentences').find({ files : { $size : 2 }})


# { files : { $size : 1 }}

# db.sentences.createIndex( { sentence : "text" } )

# db.sentences.find( { $text: { $search: "hearsay" } } )


