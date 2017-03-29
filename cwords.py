#!/usr/bin/python2.6



import os
import uuid
import sys
import re



def count_a_word(text, word, regex=False):
    if regex:
        return len(re.findall(r'%s' % word, text, re.I|re.MULTILINE|re.DOTALL))
    else:
        n = 0
        for w in text.split():
            #TODO case?
            if w.lower() == word:
                n += 1
        return n



if __name__ == '__main__':

    tmp_file = str(uuid.uuid4())
    try:
        #TODO add args check...
        #url = sys.argv[1]

        #cd = os.getcwd()
        #os.system('curl %s > %s' % (url, os.path.join(cd, tmp_file)))

        #if not os.path.exists(tmp_file):
        #    print('ERR: cannot find file: %s' % tmp_file)
        #    sys.exit(1)

        tmp_file = '/home/garryya/tmp/a.txt'

        #TODO do not read all
        text = open(tmp_file,'r').read()
        word = 'shakespeare'

        nwords = count_a_word(text, word, regex=True)

        print('%s %s''s found in text' % (nwords,word) )

    except Exception as e:
        print("Exception: %s" % e)
    finally:
        #os.unlink(tmp_file)
        pass