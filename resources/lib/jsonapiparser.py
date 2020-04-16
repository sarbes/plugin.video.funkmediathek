# -*- coding: utf-8 -*-
import requests
baseUrl = 'https://www.funk.net/api/v4.0'


#v3.0
#auth = 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJjbGllbnROYW1lIjoiY3VyYXRpb24tdG9vbCIsInNjb3BlIjoic3RhdGljLWNvbnRlbnQtYXBpLGN1cmF0aW9uLWFwaSxzZWFyY2gtYXBpIn0.'
#auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoiY3VyYXRpb24tdG9vbCIsInNjb3BlIjoic3RhdGljLWNvbnRlbnQtYXBpLGN1cmF0aW9uLWFwaSxzZWFyY2gtYXBpIn0.q4Y2xZG8PFHai24-4Pjx2gym9RmJejtmK6lMXP5wAgc'
#v3.1
#auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoiY3VyYXRpb24tdG9vbC12Mi4wIiwic2NvcGUiOiJzdGF0aWMtY29udGVudC1hcGksY3VyYXRpb24tc2VydmljZSxzZWFyY2gtYXBpIn0.SGCC1IXHLtZYoo8PvRKlU2gXH1su8YSu47sB3S4iXBI'
#v4.0
auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoid2ViYXBwLXYzMSIsInNjb3BlIjoic3RhdGljLWNvbnRlbnQtYXBpLGN1cmF0aW9uLWFwaSxuZXh4LWNvbnRlbnQtYXBpLXYzMSx3ZWJhcHAtYXBpIn0.mbuG9wS9Yf5q6PqgR4fiaRFIagiHk9JhwoKES7ksVX4'

headers = {
			'Authorization':auth,
			'Accept-Encoding':'gzip',
			}

class parser:
	def __init__(self):
		self.result = {'items':[],'pagination':{'currentPage':0}}
		self.i = 0

	def parseChannels(self,showTypes=['series']):
		j = requests.get(f'{baseUrl}/channels/?size=200', headers=headers).json()
		for item in j['_embedded']['channelDTOList']:
			if item['type'] in showTypes:
				if self.i != 0: print(item)
				self.i+=1
				d = {'type':'show', 'params':{'mode':'listSeasons'}, 'metadata':{'art':{}}}
				d['metadata']['name'] = item['title']
				if 'shortDescription' in item:
					d['metadata']['plotoutline'] = item['shortDescription']
					d['metadata']['plot'] = item['shortDescription']
				if 'description' in item:
					d['metadata']['plot'] = item['description']
				d['metadata']['art']['thumb'] = item['imageUrlSquare']
				#d['metadata']['art']['poster'] = item['imageUrlSquare']
				if 'imageUrlOrigin' in item:
					d['metadata']['art']['fanart'] = item['imageUrlOrigin']
				d['params']['alias'] = item['alias']
				if item['type'] == 'series':
					d['params']['mode'] = 'listSeasons'
				elif item['type'] == 'format':
					d['params']['mode'] = 'listVideos'
				elif item['type'] == 'archiveformat':
					d['params']['mode'] = 'listVideos'
				else:
					#print('Unknown show type: '+item['type'])
					pass
				self.result['items'].append(d)
		self.result['content'] = 'tvshows'
		return self.result	
	
	def parseSeasons(self,alias):
		j = requests.get(f'{baseUrl}/playlists/byChannelAlias/{alias}?sort=language,ASC', headers=headers).json()
		#response = libMediathek.getUrl(base+'/content/playlists/filter/?channelId=' + id + '&secondarySort=alias,ASC',header)
		#https://www.funk.net/api/v3.1/webapp/playlists/byChannelAlias/alles-liebe-annette?sort=language,ASC
		#https://www.funk.net/api/v4.0/playlists/byChannelAlias/orange-is-the-new-black-1248?sort=language,ASC
	
		for item in j['_embedded']['playlistDTOList']:
			d = {'type':'season', 'params':{'mode':'listEpisodes'}, 'metadata':{'art':{}}}
			d['metadata']['name'] = item['title']
			if 'shortDescription' in item:
				d['metadata']['plotoutline'] = item['shortDescription']
				d['metadata']['plot'] = item['shortDescription']
			if 'description' in item:
				d['metadata']['plot'] = item['description']

			if 'imageUrlPortrait' in item:
				d['metadata']['art']['thumb'] = item['imageUrlPortrait']
				d['metadata']['art']['poster'] = item['imageUrlPortrait']
			else:
				d['metadata']['art']['thumb'] = item['imageUrlLandscape']
				d['metadata']['art']['poster'] = item['imageUrlLandscape']
				
			if 'imageUrlOrigin' in item:
				d['metadata']['art']['fanart'] = item['imageUrlOrigin']
			elif 'imageUrlLandscape' in item:
				d['metadata']['art']['fanart'] = item['imageUrlLandscape']

			d['params']['alias'] = item['alias']
			self.result['items'].append(d)
		self.result['content'] = 'seasons'
		return self.result
		
	def parseEpisodes(self,alias):
		#response = libMediathek.getUrl(base+'/content/playlists/'+id+'/videos/?size=100&secondarySort=episodeNr,ASC',header)
		#https://www.funk.net/api/v3.1/webapp/videos/byPlaylistAlias/alles-liebe-annette-staffel-1?filterFsk=false&size=100&sort=episodeNr,ASC
		#response = libMediathek.getUrl(base+'/videos/byPlaylistAlias/'+id+'?filterFsk=false&size=100&sort=episodeNr,ASC',header)
		#j = json.loads(response)
		j = requests.get(f'{baseUrl}/videos/byPlaylistAlias/{alias}?filterFsk=false&size=100&sort=episodeNr,ASC', headers=headers).json()
		for item in j['_embedded']['videoDTOList']:
			d = {'type':'episode', 'params':{'mode':'playVideo'}, 'metadata':{'art':{}}}
			d['metadata']['name'] = item['title']
			if 'shortDescription' in item:
				d['metadata']['plotoutline'] = item['shortDescription']
				d['metadata']['plot'] = item['shortDescription']
			if 'description' in item:
				d['metadata']['plot'] = item['description']

			#d['_thumb'] = item['imageUrlOrigin']
			d['metadata']['art']['thumb'] = item['imageUrlLandscape']
			d['metadata']['duration'] = item['duration']
			if 'seasonNr' in item:
				d['metadata']['season'] = item['seasonNr']
			if 'episodeNr' in item:
				d['metadata']['episode'] = item['episodeNr']
			if 'fsk' in item:
				d['metadata']['mpaa'] = 'FSK ' + str(item['fsk'])
			d['params']['entityId'] = str(item['entityId'])
			self.result['items'].append(d)
		self.result['content'] = 'episodes'
		return self.result
		
	def parseVideos(self,alias):
		#https://www.funk.net/api/v3.0/content/videos/filter?channelId=auf-einen-kaffee-mit-moritz-neumeier&page=0&size=20
		#response = libMediathek.getUrl(base+'/content/videos/filter?channelId='+id+'&page=0&size=100',header)
		#https://www.funk.net/api/v3.1/webapp/playlists/byChannelAlias/auf-einen-kaffee-mit-moritz-neumeier?sort=language,ASC
		#https://www.funk.net/api/v3.1/webapp/videos/byChannelAlias/auf-einen-kaffee-mit-moritz-neumeier?filterFsk=false&sort=creationDate,desc&page=0&size=20
		#response = libMediathek.getUrl(base+'/videos/byChannelAlias/'+id+'?filterFsk=false&sort=creationDate,desc&page=0&size=100',header)
		#j = json.loads(response)
		j = requests.get(f'{baseUrl}/videos/byChannelAlias/{alias}?filterFsk=false&sort=creationDate,desc&page=0&size=100', headers=headers).json()
		for item in j['_embedded']['videoDTOList']:
			d = {'type':'video', 'params':{'mode':'playVideo'}, 'metadata':{'art':{}}}
			d['metadata']['name'] = item['title']
			if 'shortDescription' in item:
				d['metadata']['plotoutline'] = item['shortDescription']
				d['metadata']['plot'] = item['shortDescription']
			if 'description' in item:
				d['metadata']['plot'] = item['description']
			if 'imageUrlOrigin' in item:
				d['metadata']['art']['thumb'] = item['imageUrlOrigin']
			elif 'imageUrlLandscape' in item:
				d['metadata']['art']['thumb'] = item['imageUrlLandscape']
			d['metadata']['duration'] = item['duration']
			if 'fsk' in item:
				d['metadata']['mpaa'] = 'FSK ' + str(item['fsk'])
			d['params']['entityId'] = str(item['entityId'])
			self.result['items'].append(d)
		self.result['content'] = 'videos'
		return self.result