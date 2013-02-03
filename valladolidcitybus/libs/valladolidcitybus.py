#!/usr/bin/env python
# -*- coding: utf8 -*- 
from bs4 import BeautifulSoup
import urllib2
from slugify import slugify
from linecolors import linecolor
import os
import urllib
from caching import cache_disk

#~ Autobuses Valladolid
#~ Lineas
#~ Ruta
#~ Paradas -> proxima llegada

LONG_CACHING = 60 * 100


class CityBus(object):
	city = 'valladolid'
	master_url = 'http://www.auvasa.es/lineas.asp'
	
	
	def get_html(self):
		page=urllib2.urlopen(self.master_url)
		soup = BeautifulSoup(page.read())
		return soup.select(".style71 > table")

	def lines(self, line_id=None):

		lines_obj = []
		for table in self.get_html():
			#~ group = dict(
				#~ slug = slugify(table.select('.style20')[0].string),
				#~ description = table.select('.style20')[0].string
				#~ )
			#~ links = table.find_all('a')
			group = table.select('.style20')[0].string
			for link in table.find_all('a'):
				#~ new_line = Line()
				
				new_line = Line(id=link['href'].replace('lineas.asp?lin=',''))
				new_line.title = link.string
				new_line.slug = slugify(link.string)
				new_line.group = dict(
								slug = slugify(group),
								description = group
								)
				if line_id == new_line.id:
					return new_line
				lines_obj.append(new_line)
			#~ group['lines'] = 
		return lines_obj

class Line(object):
	master_url = 'http://www.auvasa.es/lineas.asp?lin=%s'
	image_url = 'http://www.auvasa.es/images/corresp/%s.jpg'
	image_path = 'images/%s.jpg'
	
	def __init__(self, *args, **kwargs):
		self.id = kwargs['id']
		self.url = self.master_url % self.id
		self.color = self._color()
	
	def __repr__(self):
		return "Line %s" % self.id

	@cache_disk(seconds = LONG_CACHING)
	def _color(self):
		if os.path.exists(self.image_path % self.id) == False:
			urllib.urlretrieve(self.image_url % self.id, self.image_path % self.id)
		return '#%s' % linecolor(self.image_path % self.id)

	@cache_disk(seconds = LONG_CACHING)
	def routes(self):
		page=urllib2.urlopen(self.url)
		soup = BeautifulSoup(page.read())
		maintables = soup.select("#column_l")[0].select('td')
		#~ print len(maintables)
		links_r = maintables[0].select('a')
		links_l = maintables[2].select('a')
		#~ print len(links_r)
		#~ print len(links_l)
		return [self.create_route(links_l), self.create_route(links_r)]

	@cache_disk(seconds = LONG_CACHING)
	def create_route(self, htmllist):
		route_list = []
		for k, item in enumerate(htmllist):
			if 'parada' in item['href']:
				#~ print item['href']
				new_stop = Stop()
				new_stop.id = item['href'].split('=')[1].split('&')[0]
				new_stop.address = item['href'].split('=')[-1]
				new_stop.correspondences = []
				route_list.append(new_stop)
			elif 'lin' in item['href']:
				#~ print('corrr>', item['href'])
				#~ print item_corr['href']
				new_corrstop = Stop()
				new_corrstop.id = item['href'].split('=')[1].split('&')[0]
				new_corrstop.address = item['href'].split('=')[-1]
						
				new_stop.correspondences.append(new_corrstop)
		return route_list
		
def Route(object):
	pass
	
class Stop(object):
	check_url = 'http://www.auvasa.es/parada.asp?codigo=%s'
		
	def __repr__(self):
		return "Stop %s" % self.id

	def get_soup(self, stop_id):
		page=urllib2.urlopen(self.check_url % stop_id)
		soup = BeautifulSoup(page.read())
		return soup.select("#sidebartiempos")[0].select('.style36')
		
	def check(self, stop_id=None, line_id=None):
		for table in self.get_soup(stop_id):
			cols = table.select('td')
			if cols[0].string == line_id:
				if cols[2].string == '0':
					return '<strong>&rarr;</strong>'
				return "%s mins." % cols[2].string
		return "!"
		
#~ auvasa = CityBus()
#~ for fu in auvasa.lines()[0].routes():
	#~ if len( fu ) > 0:
		#~ print ('ruta> ', fu)
		#~ for stop in fu:
			#~ print ('parada> ', stop)
			#~ print stop.correspondences
#~ print auvasa.lines()


