'''
General-purpose module used to format the output.
'''

import re

def elim_space(text):
    return re.sub(r'\s+', '', text)
