import urllib.request
import index

from index import *

class Crawler(object):

    def __init__(self, seed, index):
    	self.seed = seed
        self.index = index

    def crawl(self, seed):

    	to_crawl = [seed]
    	crawled = []

    	for url in to_crawl:

    		page = get_page(url)
    		links = get_all_links(page)
    		kws = page.lower().split(" ")

    		for i in range(len(links)):
    			links[i] = repair_link(links[i])

    		for kw in kws:
    			for link in links:
    				self.index.add(kw, link)

    		crawled.append(url)
    		
    		for link in links:
    			if not(link in crawled or link in to_crawl):
    				to_crawl.append(link)

    		to_crawl.pop(0)


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
	        url, end = get_next_target(page, start)
	        # on recommence la prochaine recherche depuis la fin du résultat courant
	        start = end
	        
	        if url is not None:
	            urls.append(url)
	    
	    return urls
	    
	@staticmethod
	def repair_link(source_url, link):

		if link.find("#") == -1 and link != "": # Filtrage des ancrages et des urls vides

			if link[0] = "/": # Réparation des liens relatifs à la racine du site
				root = source_url[0 : source_url.find("/", 7)]
				link  = root + link

			elif link[0:4] != "http": # Réparation des liens relatifs à la page actuelle
				folder = source_url[0 : source_url.rfinf("/") + 1]
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

    	else:
    		page = ''

    	return page


