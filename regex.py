import re


replecament_patterns = [(r'won\'t','will not'),
                        (r'can\'t','can not'),
                        (r'don\'t','do not'),
                        (r'didn\'t','did not'),
                        (r'doesn\'t','does not'),
                        (r'couldn\'t','could not'),
                        (r'wouldn\'t','would not'),
                        (r'shouldn\'t','should not'),
                        (r'haven\'t','have not'),
                        (r'hasn\'t','has not'),
                        (r'hadn\'t','had not'),
                        (r'isn\'t','is not'),
                        (r'aren\'t','are not'),
                        (r'wasn\'t','was not'),
                        (r'weren\'t','were not')]

class RegexReplacer(object):
    def __init__(self,patterns=replecament_patterns):
        self.patterns = [(re.compile(regex),repl) for (regex,repl) in patterns]

    def replace(self,text):
        global s
        s = text
        for(pattern,repl) in self.patterns:
            s = re.sub(pattern,repl,s)
        return s
