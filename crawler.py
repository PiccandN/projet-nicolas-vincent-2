import urllib.request
import indexer

class Crawler(object):

    def __init__(self):
        self.index = indexer.SearchIndex()
        
    def crawl(self, seed, debug = False):

        self.to_crawl = [seed]
        self.crawled = []
        self.debug = debug

        for url in self.to_crawl:

            page = Crawler.get_page(url)
            links = Crawler.get_all_links(page)
            kws = Crawler.clean_kws(page)

            for i in range(len(links)):
                links[i] = Crawler.repair_link(url, links[i])

            for kw in kws:
                self.index.add(kw, url)

            self.crawled.append(url)
            
            for link in links:
                if not(link in self.crawled or link in self.to_crawl):
                    self.to_crawl.append(link)

            
            if self.debug:
                print("\n------------ to_crawl ------------")
                Debug.print_list(self.to_crawl)
                print("\n------------ crawled ------------")
                Debug.print_list(self.crawled)
                print("\n*******************************************************************************\n")

        if self.debug:
            Debug.print_index(self.index)


    @staticmethod
    def get_all_links(page):
        '''
        
        Retourne tous les hyperliens contenus dans la chaine de caractères ``html``
        sous forme d'une liste. 
        
        Si la page ne contient aucun lien, la fonction retourne la liste vide.
        
        paramètres
        ==========
        
        * html ==> str : code HTML de la page dont on veut extraire les liens
        
        Valeur de retour
        ================
        
        Liste contenant les liens (urls) et une liste vide si 
        la page ne contient aucun lien


        Copier-coller de https://c9.io/csud_oci/oci-projet-demo
        
        '''
        
        start = 0
        urls = []
        
        if len(page) == 0:
            return []
            
        while start != -1:
            url, end = Crawler.get_next_target(page, start)
            # on recommence la prochaine recherche depuis la fin du résultat courant
            start = end
            
            if url is not None:
                urls.append(url)
        
        return urls
    
    @staticmethod
    def clean_kws(txt):
        kws = txt.lower().split(" ")

        for i in range(len(kws)):
            if len(kws[i]) <= 2:
                kws.pop(i)





    @staticmethod
    def repair_link(source_url, link):

        if link.find("#") == -1 and link != "": # Filtrage des ancrages et des urls vides

            if link[0] == "/": # Réparation des liens relatifs à la racine du site
                root = source_url[0 : source_url.find("/", 7)]
                link  = root + link

            elif link[0:4] != "http": # Réparation des liens relatifs à la page actuelle
                folder = source_url[0 : source_url.rfind("/") + 1]
                link = folder + link

        return link


    @staticmethod
    def get_next_target(page, start = 0):
        '''
    
        Retourne une tuple (url, end) où url est 
        l'URL (target) du premier lien rencontré dans le 
        code HTML ``page`` à partir de la position
        ``start`` et ``end`` indique la position de la
        fin de l'URL dans ``page``.
        
        S'il n'y a plus de lien après la position start, 
        la fonction retourne le tuple (None, -1).

        '''
        
        pattern = '<a href="'
        start_tag = page.find(pattern, start)
        
        if start_tag == -1:
            return (None, -1)
        
        else:
            start_url = start_tag + len(pattern)
            end_url = page.find('"', start_url)
            
            url = page[start_url:end_url]
            
            return (url, end_url+1)


    @staticmethod
    def get_page(url):
        '''
        Récupère le contenu d'une page HTML située à une url donnée.
        Retourn une chaîne de caractère, vide en cas d'erreur.

        '''

        try:
            html = urllib.request.urlopen(url).read()
            page = str(html)

        except:
            page = ''

        return page


class Debug(object):

    @staticmethod
    def print_list(ls):

        for e in ls:
            print(e)

    @staticmethod
    def print_index(index):

        for kw in index.entries:
            print('"' + str(kw) + '"')
            Debug.print_dict(index.entries[kw].urls)

    @staticmethod
    def print_dict(dico):

        for e in dico:
            print(str(e) + " : " + str(dico[e]))
