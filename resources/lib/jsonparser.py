# -*- coding: utf-8 -*-
import json
import requests

baseUrl = 'https://www.funk.net/data/static'
baseUrlApi = 'https://www.funk.net/api/v4.0/'


class parser:
	def __init__(self):
		self.result = {'items':[],'pagination':{'currentPage':0}}
		
	def parseLatest(self):
		j = requests.get(f'{baseUrl}/latestVideos').json()
		for item in j['list']:
			d = {'type':'video', 'params':{'mode':'playVideo'}, 'metadata':{'art':{}}}
			d['metadata']['name'] = item['title']
			d['metadata']['plotoutline'] = item['shortDescription']
			d['metadata']['plot'] = item['shortDescription']
			if 'episodeNr' in item:
				d['metadata']['episode'] = item['episodeNr']
			if 'seasonNr' in item:
				d['metadata']['season'] = item['seasonNr']
			d['metadata']['art']['thumb'] = f"{baseUrlApi}/thumbnails/{item['imageLandscape']}?quality=85&width=220"
			d['params']['entityId'] = item['entityId']
			self.result['items'].append(d)
		self.result['content'] = 'videos'
		return self.result

	def parseMixes(self):
		j = requests.get(f'{baseUrl}/mixes').json()
		for item in j['list']:
			d = {'type':'dir', 'params':{'mode':'listEpisodes'}, 'metadata':{'art':{}}}
			d['metadata']['name'] = item['title']
			d['metadata']['plotoutline'] = item['description']
			d['metadata']['plot'] = item['description']
			#d['metadata']['videoCount'] = item['videoCount']
			d['metadata']['art']['thumb'] = f"{baseUrlApi}/thumbnails/{item['imageCover']}?quality=85&width=220"
			d['params']['alias'] = item['alias']
			self.result['items'].append(d)
		self.result['content'] = 'tvshows'
		return self.result
