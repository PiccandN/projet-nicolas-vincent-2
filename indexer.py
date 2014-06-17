class SearchIndex(object):
    

    def __init__(self):
        self.entries = {}

    def add(self, kw, url, nb_occ=1):
        '''

        Si aucune entrée correspondant à ``kw`` ne figure dans l'index,
        ajoute une entrée associant le mot-clé ``kw`` à l'url ``url``.

        Si l'index possède déjà une entrée associée au mot-clé ``kw``, ajoute
        ``url`` aux urls associées au mot-clé.

        Le paramètre ``nb_occ`` correspond au nombre d'occurrences du mot-clé
        ``kw`` dans la page indiquée par ``url```.

        '''
        
        if kw in self.entries.keys():

            entry = self.entries[kw]

            if url in self.entries[kw].get_urls():
                self.entries[kw].incr_occurence(url, nb_occ)
            else:
                self.entries[kw].add_url(url, nb_occ)

        else:
            self.entries[kw] = IndexEntry(kw)
            self.entries[kw].add_url(url, nb_occ)

    def get(self, kw):
        '''

        Retourne l'entrée correspondant au mot clé ``kw`` et None si le mot-
        clé ne figure pas dans l'index

        '''
        
        return self.entries[kw, None]
        

    def lookup(self, kw):
        '''

        Retourne la liste des urls associées au mot-clé ``kw`` et une liste
        vide si le mot-clé n'existe pas

        '''
        self.entries[kw].incr_lookups()
        
        if kw in self.entries.keys():
            return self.entries[kw].get_urls()
        else:
            return []


class IndexEntry(object):

    def __init__(self, kw, nb_lookups = 0):
        self.kw = kw
        self.nb_lookups = nb_lookups
        self.urls = {}



    def get_kw(self):
        ''' Retourne le mot-clé associé à cette entrée '''
        return self.kw

    def incr_occurence(self, url, nb_occ):
        self.urls[url] += nb_occ

    def incr_lookups(self):
        self.nb_lookups += 1

    def get_urls(self):
        ''' Retourne la liste des urls associées à cette entrée '''
        return list(self.urls.keys())


    def add_url(self, url, nb_occ=1):
        '''

        Ajoute l'url à l'entrée. Le paramètre optionnel ``nb_occ`` indique le
        nombre d'occurrences du mot-clé associé à l'entrée dans la page
        indiquée par ``url``

        '''
        self.urls[url] = nb_occ
