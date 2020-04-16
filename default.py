# -*- coding: utf-8 -*-
from libmediathek4 import lm4
import resources.lib.jsonparser as jsonparser
import resources.lib.jsonapiparser as jsonapiparser

class funk(lm4):
	def __init__(self):
		self.defaultMode = 'main'

		self.modes = {
			'main': self.main,
			'listNew': self.listNew,
			'listMixes': self.listMixes,
			'listChannels': self.listChannels,
			'listSeasons': self.listSeasons,
			'listEpisodes': self.listEpisodes,
			'listVideos': self.listVideos,
			}	
		
		self.playbackModes = {
			'playVideo':self.playVideo,
			}

		self.jp = jsonparser.parser()
		self.jap = jsonapiparser.parser()

	def main(self):
		l = []
		l.append({'metadata':{'name':self.translation(32031)}, 'params':{'mode':'listNew'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32135)}, 'params':{'mode':'listMixes'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(30504)}, 'params':{'mode':'listChannels', 'showTypes':'series'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(30503)}, 'params':{'mode':'listChannels', 'showTypes':'format,archiveformat'}, 'type':'dir'})
		#l.append({'metadata':{'name':'listChannels archiveformat'}, 'params':{'mode':'listChannels', 'showTypes':'archiveformat'}, 'type':'dir'})
		return {'items':l,'name':'root'}
		
	def listNew(self):
		return self.jp.parseLatest()
		
	def listMixes(self):
		return self.jp.parseMixes()
		
	def listChannels(self):
		return self.jap.parseChannels(self.params['showTypes'].split(','))

	def listSeasons(self):
		return self.jap.parseSeasons(self.params['alias'])
		
	def listEpisodes(self):
		return self.jap.parseEpisodes(self.params['alias'])
		
	def listVideos(self):
		return self.jap.parseVideos(self.params['alias'])
		
	def playVideo(self):
		import nexx
		#nexx.operations = {'byid':'2835669fdcfe2d07351d633353bf87a8'}
		#nexx.operations = {'byid':'f058a27469d8b709c3b9db648cae47c2'}
		nexx.operations = {'byid':'137782e774d7cadc93dcbffbbde0ce9c'}
		#nexx.cid = '114994613565243649'
		nexx.cid = '1152923389105252956'
		nexx.channelId = '741'
		nexx.origin = 'https://www.funk.net'
		return nexx.getVideoUrl(self.params['entityId'])

f = funk()
f.action()