import urllib.request
import index

from index import *

class Crawler(object):

    def __init__(self, index):
        self.index = index

    @staticmethod
    def get_all_links(page):
    	pass

    @staticmethod
    def get_next_target(page, start = 0):
    	pass

    @staticmethod
    def get_page(url):
    	'''
    	Récupère le contenu d'une page HTML située à une url donnée.
    	Retourn une chaîne de caractère, vide en cas d'erreur.

    	'''

    	try:
    		html = urllib.request.urlopen(url).read()
    		txt = str(html)

    	else:
    		txt = ''

    	return txt
    	

