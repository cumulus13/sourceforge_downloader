#!/usr/bin/env python2
from __future__ import print_function
import os, sys
import traceback
import requests
from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
if sys.platform == 'win32':
	sys.excepthook = traceback.format_exc
	from idm import IDMan
from pywget import wget
import argparse
import cmdw
import re
import json
from pprint import pprint
from pause import pause
import time
import cmdw
import clipboard
import progressbar
try:
	import treelib
	from treelib import Node, Tree
except:
	sys.exit(make_colors("Install treelib first !", 'lw', 'lr', ['blink']))
if sys.version_info.major == 3:
	from urllib.parse import unquote, quote
else:
	from urllib import unquote, quote
from operator import itemgetter

if sys.version_info.major == 3:
	raw_input = input
	import urllib.parse as urllib
else:
	import urlparse
	
class Flower(object):
	def __init__(self, color):
		self.color = color
		self.n_same_files = 0
	
class sourceforge(object):
	def __init__(self):
		super(sourceforge, self)
		self.session = requests.Session()
		self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
		self.session.headers.update(self.headers)		
		self.url = "https://sourceforge.net/"
		self.level = 100000
		self.bar_prefix = "{variables.task} >> {variables.subask}"
		self.bar_variables = {'task':'--', 'subtask':'--'}
		self.bar_max_value = 10
		self.bar = progressbar.ProgressBar(self.bar_max_value, prefix = self.bar_prefix, variables = self.bar_variables)
		
	def del_evenReadonly(self, action, name, exc):
		task = make_colors('DIFFC REMOVE', 'lw', 'lr')
		subtask = make_colors(str(name), 'b', 'ly')
		self.bar.update(1, task = task, subtask = subtask, max_value=10)
		n = 1
		while 1:
			try:
				import stat
				os.chmod(name, stat.S_IWRITE)
				os.remove(name)
				self.bar.update(10, task = task, subtask = subtask, max_value=10)
				break
			except:
				if n == 10:
					break
				else:
					self.bar.update(n, task = task, subtask = subtask, max_value=10)
					n+=1
		
	def download(self, url, download_path=os.getcwd(), saveas=None, debugx = False, max_try=10, clip = False, downloadit = False):
		headers = {
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
			'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'accept-language':'en-US,en;q=0.5',
			'upgrade-insecure-requests':'1',
			'te':'trailers',
			'accept-encoding':'gzip, deflate'
		}
		
		debug(headers = headers, debug = debugx)
		self.session.headers.update(headers)
		try:
			a = self.session.get(url, headers = headers)
		except:
			a = self.session.get(url, headers = headers, verify=False)
		debug(sess_headers = a.headers, debug = debugx)
		
		content = a.content
		
		b = bs(content, 'lxml')
		meta = b.find_all('meta', {'http-equiv':re.compile('refresh')})
		debug(meta = meta, debug = debugx)
		if meta:
			meta_content = meta[0].get('content')
			debug(meta_content = meta_content)
			link = re.findall('url=(.*?)$', meta_content)[0]
			debug(link = link, debug = debugx)
			debug(headers = headers, debug = debugx)
			headers.update({'referer': url})
			debug(headers = headers, debug = debugx)
			self.session.headers.update(headers)
			project_name = re.findall('projects/(.*?)/', url)
			debug(project_name = project_name, debug = debugx)
			path = re.findall('files/(.*?)/download', url)
			debug(path = path, debug = debugx)
			cookies = {}
			if not saveas:
				saveas_path = urlparse.urlparse(link).path
				if saveas_path:
					saveas = re.split("/", saveas_path)[-1]
			debug(saveas = saveas, debug = True)
			# if saveas:
			# 	saveas = ''
			if not saveas:
				try:
					saveas = os.path.split(path[0])[1]
				except:
					pass
			debug(saveas = saveas, debug = True)
			if not saveas:
				saveas = re.split("/", link)[-1]
				debug(saveas = saveas, debug = debugx)
				saveas = re.findall('(.*?)\?r=', saveas)
				debug(saveas = saveas, debug = debugx)
				if saveas:
					saveas = saveas[0]
			debug(saveas = saveas, debug = True)
			if project_name and path:
				cookies = {'sf_mirror_attempt':project_name[0] + ":master:" + path[0]}
				debug(cookies = cookies, debug = debugx)
				headers.update({'Cookie':'sf_mirror_attempt=' + project_name[0] + ":master:" + path[0]})
				debug(headers = headers, debug = debugx)
				self.session.headers.update(headers)
			# pause()
			if clip:
				clipboard.copy(link)
			if downloadit:
				try:
					if sys.platform == 'win32':
						from idm import IDMan
						dm = IDMan()
						return dm.download(link, download_path, saveas, cookie=str(cookies))
					else:
						import download
						return download.download(link, download_path, saveas)	
				except:
					traceback.format_exc()
					qq = raw_input(make_colors("Do you want to continue [y/e[n]ter:", 'lw', 'r') + " ")
					if qq == 'y' or qq == 'yes':
						import download
						return download.download(link, download_path, saveas)
	
	def download_latest(self, url, download_path=os.getcwd(), saveas=None, clip = False, downloadit = False):
		if 'projects' in re.split("/", url):
			url = re.split(self.url, url)
			debug(url = url)
			if len(url) > 1:
				url = url[1]
			else:
				url = url[0]
			debug(url0 = url)
			if len(re.split("/", url)) == 5 and 'sourceforge.net' in url:
				url = url + "/files/latest/download"
				debug(url = url)
				return self.download(url, download_path, saveas)
			if "/" == url[0]:
				url = "/".join(re.split("/", url[1:])[:2])
				debug(url1 = url)
			else:
				url = "/".join(re.split("/", url)[:2])
				debug(url2 = url)
			url = self.url + url + "/files/latest/download"
			debug(url = url)
			
			return self.download(url, download_path, saveas, clip = clip, downloadit = downloadit)
		else:
			print(make_colors("download latest failed !", 'lw', 'lr', ['blink']))
			return None
		
	def get_os(self):
		if sys.platform == 'win32':
			return 'windows'
		elif sys.platform == 'darwin':
			return 'macos'
		else:
			return 'linux'
	
	def clean(self, data):
		if sys.version_info.major == '3':
			f = filter(None, data)
			return [i for i in f]
		else:
			return filter(None, data)
			
	def print_tree_files(self, url = None, data_tree = None, root=None, level = 1, print_list=False, bs_object=None, folders = None, files = None, data_dict =None, n_same_files = 1, n_same_folders = 1):
		data_bank_dict = {}
		data_bank_name_dict = {}
		nb = 0
		def add(folders, files, data_tree, root, n_same_files = 1, n_same_folders = 1, super_root = '/', nb = 0):
			self.n_same_files = n_same_files
			self.n_same_folders = n_same_folders
			debug(folders = folders)
			for i in folders:
				debug(i_folder = i)
				debug(root = root)
				
				if not data_tree.get_node(root):
					data_tree.create_node(make_colors(root, 'lw', 'lr'), root, parent = super_root)
				try:
					data_tree.create_node(make_colors(i.get('title'), 'ly') + " " + make_colors("[" + str(nb) + "]", 'lw', 'lr'), i.get('title'), parent = root, data = i)
				except treelib.tree.DuplicatedNodeIdError:
					try:
						data_tree.create_node(make_colors(i.get('title'), 'ly') + " " + make_colors("[" + str(nb) + "]", 'lw', 'lr'), i.get('title') + "-" + str(n_same_folders), parent = root, data = i)
						n_same_folders += 1
					except treelib.tree.DuplicatedNodeIdError:
						debug(data_tree = data_tree)
						data_tree.show()
						traceback.format_exc()
						sys.exit(treelib.tree.DuplicatedNodeIdError)
				if i.get('title'):
					data_bank_name_dict.update({nb: i.get('title'),})
					nb += 1									
			debug(data_tree = data_tree)
			#data_tree.show()
			for i in files:
				debug(i_file = i)
				debug(root = root)
				
				if not data_tree.get_node(root):
					data_tree.create_node(make_colors(root, 'lw', 'lr'), root,  parent = super_root)				
				try:
					data_tree.create_node(make_colors(i.get('title'), 'lc') + " " + make_colors("[" + str(nb) + "]", 'lw', 'lr'), i.get('title'), parent= root, data = i)
				except:
					data_tree.create_node(make_colors(i.get('title'), 'lg') + " " + make_colors("[" + str(nb) + "]", 'lw', 'lr'), i.get('title') + "-" + str(n_same_files), parent= root, data = i)
					debug(root = root)
					n_same_files += 1
					self.n_same_files = n_same_files
				if i.get('title'):
					data_bank_name_dict.update({nb: i.get('title'),})
					nb += 1								
			debug(data_tree = data_tree)
			#data_tree.show()			
			return data_tree, n_same_files, n_same_folders, nb
		
		debug(data_tree = data_tree)
		if not root:
			root = '/'
		if not data_tree:
			data_tree = Tree()
			data_tree.create_node(root, root)
		debug(url = url)
		debug(root = root)
		folders_1 = []
		files_1 = []
		data_dict_1 = {}
		
		if not folders or not files:
			folders, files, data_dict = self.get_files(url)
			data_bank_dict.update(data_dict)
			debug(folders = folders)
			debug(files = files)
			debug(data_dict = data_dict)
		data_bank_name_dict.update({nb: root,})
		nb += 1		
		while 1:
			nd = 1
			nf = 1			
			sub_folders_all = {}
			sub_files_all = {}			
			if level == 0:
				#data_tree.show()
				break
			else:
				#data_dict = []
				if isinstance(folders, list):
					debug(folders = folders)
					for i in folders:
						debug(i = i)
						link = self.url + i.get('link')[1:]
						debug(link = link)
						debug(self_url = self.url)
						folders_1, files_1, data_dict_1 = self.get_files(link)
						data_bank_dict.update(data_dict_1)
						sub_folders_all.update({nd: folders_1,})
						sub_files_all.update({nf: files_1,})
						nd += 1
						nf += 1
						data_tree, n_same_files, n_same_folders, nb = add(folders_1, files_1, data_tree, i.get('title'), n_same_files, n_same_folders, root, nb)
					folders = sub_folders_all
					debug(folders = folders)
					files = sub_files_all
				elif isinstance(folders, dict):
					for i in folders:
						for x in folders.get(i):
							link = self.url + x.get('link')[1:]
							debug(link = link)
							debug(self_url = self.url)
							folders_1, files_1, data_dict_1 = self.get_files(link)
							data_bank_dict.update(data_dict_1)
							sub_folders_all.update({nd: folders_1,})
							sub_files_all.update({nf: files_1,})
							nd += 1
							nf += 1
							data_tree, n_same_files, n_same_folders, nb = add(folders_1, files_1, data_tree, x.get('title'), n_same_files, n_same_folders, root, nb)
					folders = sub_folders_all
					files = sub_files_all
				debug(level = level)
				if isinstance(level, list) and not level:
					break
				else:
					level = int(level) - 1
				debug(level = level)
		if print_list:
			data_tree.show()
		return data_tree, data_bank_dict, data_bank_name_dict
	
	def get_subtree(self, node, data_tree):
		data = None
		try:
			data = data_tree.subtree(node)
		except:
			pass
		try:
			if self.n_same_files:
				for i in range(self.n_same_files + 1):
					try:
						data = data_tree.subtree(node + "-" + str(i))
					except:
						pass
		except:
			pass
		return data
					
	def get_files(self, url = None, bs_object = None):
		if not url and not bs_object:
			return {}
		if not bs_object:
			while 1:
				try:
					a = requests.get(url)
					break
				except:
					time.sleep(1)
			content = a.content
			with open('result.html', 'wb') as f:
				f.write(content)
			bs_object = bs(content, 'lxml')
		b = bs_object
		all_scripts = b.find_all('script')
		net_sf_files = ''
		for i in all_scripts:
			if "net.sf.files" in i.text:
				net_sf_files = re.findall('net\.sf\.files = (.*?);', i.text)
				debug(net_sf_files = net_sf_files)
				break
		if net_sf_files:
			net_sf_files = json.loads(net_sf_files[0])
		debug(net_sf_files = net_sf_files)
		#pprint(net_sf_files)
		
		#if net_sf_files:
			#return net_sf_files
			
		table = b.find('table', {'id':'files_list'})
		debug(table = table)
		if not table:
			return [], [], {}
		folders = []
		files = []
		all_tr_folders = table.find_all('tr', {'class':'folder'})
		all_tr_files = table.find_all('tr', {'class':'file'})
		if all_tr_folders:
			for i in all_tr_folders:
				debug(i = i)
				if i.find('a', title = re.compile('Click to enter')):
					title = i.get('title')
					link = i.find('a', title = re.compile('Click to enter')).get('href')
					date = i.find('td', {'headers':'files_date_h'}).find('abbr').get('title')
					folders.append({'title':title, 'date':date, 'link':link})
		if all_tr_files:
			for i in all_tr_files:
				title = i.get('title')
				link = i.find('a', title = re.compile('Click to download')).get('href')
				date = i.find('td', {'headers':'files_date_h'}).find('abbr').get('title')
				size = i.find('td', {'headers':'files_size_h'}).text
				files.append({'title':title, 'date':date, 'link':link, 'size':size})
			
		debug(folders = folders)
		#clipboard.copy(str(folders))
		debug(files = files)
		folders = sorted(folders, key = lambda k: k['date'], reverse = True)
		files = sorted(files, key = lambda k: k['date'], reverse = True)
		return folders, files, net_sf_files
				
	def search(self, query):
		suggest_url = self.url + "proxy-api/search/suggest-project"
		search_url = self.url + "directory/os:{0}/".format(self.get_os())
		debug(suggest_url = suggest_url)
		debug(search_url = search_url)
		params = {'q':query}
		debug(params = params)
		
		try:
			suggest_content = requests.get(suggest_url, params = params).json()
		except:
			try:
				import json
				a = requests.get(suggest_url, params = params)
				suggest_content = json.loads(a.text)
			except:
				sys.exit(make_colors("Connection Error !", 'lw', 'lr',  ['blink']) +  " " + make_colors("[no internet connection]",  'lr',  'ly'))
				
		debug(suggest_content = suggest_content.get('response'))
		search_content = requests.get(search_url, params = params).content
		#print("search_content =", search_content)
		b = bs(search_content, 'lxml')
		all_li = b.find_all('li', {'itemprop':'itemListElement'})
		debug(all_li = all_li)
		data = {}
		n = 1
		for i in all_li:
			link = i.find('a', {'title':re.compile("Find out more about")})
			if link:
				debug(link = link)
				link0 = link.get('href')
				title = re.sub("Find out more about ", '', link.get('title'))
				data.update({
					n : {
							'title': title, 
							'link': self.url + link0[1:],
						}
				})
				n+=1
		page = self.pagination(b)
		debug(data = data)
		return data, page
		
	def details(self, url):
		description = ''
		a = requests.get(url)
		b = bs(a.content, 'lxml')
		p_description = b.find('p', {'itemprop':'description'})
		debug(p_description = p_description)
		if p_description:
			homepage = p_description.find('a')
			debug(homepage = homepage)
			if homepage:
				homepage = homepage.get('href')
			debug(homepage = homepage)
			description = p_description.text
			debug(description = description)
		features = []
		ul_features = b.find('ul', {'class':'features as-columns'})
		debug(ul_features = ul_features)
		if ul_features:
			all_li = ul_features.find_all('li')
			debug(all_li = all_li)
			for i in all_li:
				features.append(i.text)
		debug(features = features)
		screenshot = []
		videos = []
		all_screenshot = b.find_all('a', {'class':'gallery'})
		debug(all_screenshot = all_screenshot)
		if all_screenshot:
			for i in all_screenshot:
				if i.find('img').get('alt') == 'Play Video':
					videos.append('https:' + i.get('href'))
				else:
					screenshot.append('https:' + re.findall("(.*?)/max", i.get('href'))[0])
		debug(screenshot = screenshot)
		debug(videos = videos)
		icon = b.find('img', itemprop='image')
		debug(icon = icon)
		if icon:
			icon = icon.get('src')
		debug(icon = icon)
		if icon:
			icon = 'https:' + icon
		title = b.find('h1', itemprop="name")
		debug(title = title)
		if title:
			title = title.text
		debug(title = title)
		return title, description, features, screenshot, icon, videos
		
	def pagination(self, bs_object=None, url=None, max_try = 5):
		if url:
			a = requests.get(url)
			b = bs(a.content, 'lxml')
		else:
			b = bs_object
		if not bs_object and not url:
			return {}
		debug(url = url)
		n = 0
		error = False
		while 1:
			try:
				ul_page = b.find('ul', {'class':'pagination text-center'})
				all_li = ul_page.find_all('li')
				break
			except:
				try:
					debug(ul_page = ul_page)
				except:
					pass
				if n == max_try:
					error = True
					break
				else:
					sys.stdout.write(".")
					n += 1
		if error:
			return {}
		current = ul_page.find('li', {'class':'current'})
		debug(current = current)
		if current:
			current = re.sub("You're on page ", '', current.text).strip()
		debug(current = current)
		next = ul_page.find('a', {'aria-label':re.compile('Next page')})
		debug(next = next)
		if next:
			next = {'link':next.get('href'), 'page': re.findall('.*?page=(.*?)$', next.get('href'))[0]}
			debug(next = next)
			if current:
				current_no = current
				debug(current_no = current_no)
				debug(test = re.sub(".*?page=(.*?)$", str(current_no), next.get('link')))
				current = {'link':re.sub("page=(.*?)$", "page="+ str(current_no), next.get('link')), 'page': current_no}
				debug(current = current)
				
		all_page = {}
		for i in all_li:
			npage = i.find('a', {'aria-label':re.compile("Page ")})
			if npage:
				all_page.update({npage.text:npage.get('href')})
		all_page.update({'next':next})
		all_page.update({'current':current})
		debug(all_page = all_page)
		return all_page
	
	def print_nav(self):
		note = make_colors("Select number:", 'lw', 'bl') + " " + make_colors("[n]d = latest direct download of n", 'lw', 'lr') + ", " + make_colors("[n]s = show n screenshot", 'b', 'ly') + ", " + make_colors('[n]l = list all of file for 20 files first', 'lc') + ", " + make_colors("[n]t = show all of tree file for 20 files first", 'lw', 'm') + ", " + make_colors("[n]p = goto n page", 'ly') + ", " + make_colors("s[query] | s=[query] = search for query", 'lg') + ": "
		p = raw_input(note)
		return p
	
	def navigator(self, query=None, download_path=os.getcwd(), saveas=None, print_list=True, p =None, data=None, data_files_tree=None, url_selected = None, level = 1):
		folders = None
		files = None
		level = 0
		n_sel = None
		if not query and not p:
			p = self.print_nav()
		else:
			if query:
				search_data, page = self.search(query)
				if print_list:
					for i in search_data:
						number = str(i)
						if len(number) == 1:
							number = "0" + number
						print(\
						make_colors(number, 'lm') + ". " + make_colors(search_data.get(i).get('title'), 'lw', 'bl'))
		if not p:
			p = self.print_nav()
		debug(p = p)
		if p:
			p = str(p).strip().lower()
		if p and p.isdigit() and int(p) < len(list(search_data.keys())):
			n_sel = p
			link = search_data.get(int(p)).get('link')
			debug(link = link)
			data = self.details(link)
			if not data:
				data = self.details(link)
			title, description, features, screenshot, icon, video = data
			padd = (cmdw.getWidth() - len(title) + 2) / 2
			print(int(padd) * ' ' + make_colors(title, 'lw', 'bl') + int(padd) * ' ')
			print(make_colors("Description", 'lc') + ": ")
			print(make_colors(description, 'ly'))
			print(make_colors("Features   ", 'lm') + ": ")
			
			for i in features:
				print(" " * 12 + "- " + make_colors(i, 'lw', 'm'))
			if screenshot:
				print(make_colors("Screenshot ", 'lg') + ": " + make_colors("True", 'lr', 'lw'))
			if video:
				print(make_colors("Video      ", 'lr') + ": " + make_colors("True", 'lr', 'lw'))
			p = self.print_nav()
			if p:
				if p == 'x' and p =='q':
					sys.exit()
				elif p[0].lower() == 's' or p[:2].lower() == 's=':
					query = None
				return self.navigator(query, download_path, saveas, print_list, p, data)
		elif p == 'd' or p[-1:] == 'd':
			if p == 'd':
				n_sel = raw_input(make_colors("select number to download latest: ", 'lw', 'bl'))
			else:
				n_sel = p[:-1]
			if int(n_sel) < len(list(search_data.keys())):
				link = search_data.get(int(n_sel)).get('link')
				debug(link = link)
				self.download_latest(link, download_path, saveas)
				return self.navigator(query, download_path, saveas, print_list, None, data, data_files_tree)
		elif p == 'x' or p == 'q':
			sys.exit(make_colors("SYSTEM EXIT !", 'lw', 'lr', ['blink']))
		elif p == 's' or re.findall('\\d+.*?s', p):
			if "=" in p:
				return self.navigator(None, download_path, saveas, print_list, p, data, data_files_tree)
			if p == 's':
				n_sel = raw_input(make_colors("select number to show screenshot: ", 'lw', 'bl'))
			else:
				n_sel = p[:-1]
			if not data:
				if int(n_sel) < len(list(search_data.keys())):
					link = search_data.get(int(n_sel)).get('link')
					debug(link = link)
					data = self.details(link)
			if data:
				title, description, features, screenshot, icon, video = data
				if not screenshot:
					print(make_colors("No Screenshot !", 'lw', 'lr'))
					p = self.print_nav()
					if p == 'x' and p =='q':
						sys.exit()
					return self.navigator(query, download_path, saveas, print_list, p, data, data_files_tree)
				if screenshot:
					from multiprocessing import Process
					try:
						from . import tkimage
						from . import download
					except:
						import tkimage
						import download
						
					screenshot_path = os.path.join(os.path.dirname(__file__), 'screenshot')
					if not os.path.isdir(screenshot_path):
						os.makedirs(screenshot_path)
					else:
						import shutil
						shutil.rmtree(screenshot_path, onerror=self.del_evenReadonly)
						os.makedirs(screenshot_path)
					tx0 = None
					for i in screenshot:
						tx0 = Process(target=download.download_img, args=(i, screenshot_path,
																		  False, True))
						tx0.run()
					tx = Process(target=tkimage.main, args=(screenshot_path, ))
					tx.start()
			p = self.print_nav()
			if p == 'x' and p =='q':
				sys.exit()
			return self.navigator(query, download_path, saveas, print_list, p, data, data_files_tree)
		elif p == 't' or re.findall("(\d+)t", p):
			if p == 't':
				if not n_sel:
					n_sel = raw_input(make_colors("select number to show file tree: ", 'lw', 'bl'))
				if not level:
					level = raw_input(make_colors("Level tree: ", 'lw', 'lm'))
			else:
				n_sel = re.findall("(\d+)t", p)
				if n_sel:
					n_sel = n_sel[0]
				level = re.findall("t(\d+)", p)
				if level:
					level = int(level[0])
			
			data_dict_name = {}
			data_dict = {}
			data_files_tree = None
			data_subtree = {}
			link = None
			if not url_selected:
				if int(n_sel) < len(list(search_data.keys())):
					link = search_data.get(int(n_sel)).get('link') + 'files'
					debug(link = link)
			else:
				link = url_selected
			if link:
				data_files_tree, data_dict, data_dict_name = self.print_tree_files(link, data_files_tree, print_list = True, level = level)
				debug(data_dict = data_dict)
			
			p = self.print_nav()
			if p:
				if p == 't' or re.findall("(\d+)t", p):
					print_list = False
				if p == 'x' or p == 'q':
					sys.exit()
				debug(len_data_dict = len(data_dict.keys()))
				if str(p).strip().isdigit() and not int(p) > len(data_dict.keys()):
					if data_dict_name:
						data_subtree = self.get_subtree(data_dict_name.get(int(p)), data_files_tree)
					if data_subtree:
						data_subtree.show()
						qd = raw_input(make_colors("Download it [y/enter]: ", 'lw', 'lr'))
						if qd and str(qd).strip() == 'y':
							url_selected = data_dict.get(data_dict_name.get(int(p))).get('url')
							debug(url_selected = url_selected)
							if url_selected:
								url_selected = self.url + url_selected[1:]
								self.download(url_selected, download_path, saveas)
				elif re.findall("(\d+)t", p):
					n_sel_sub = re.findall("(\d+)t", p)
					if n_sel_sub:
						n_sel_sub = n_sel_sub[0]
					level_sub = re.findall("t(\d+)", p)
					if level_sub:
						level_sub = int(level_sub[0])
					if not data_dict_name.get(int(n_sel_sub)):
						return self.navigator(query, download_path, saveas, print_list, None, data)
					url_selected = self.url + data_dict.get(data_dict_name.get(int(n_sel_sub))).get('url')[1:]
					debug(url_selected = url_selected)
					return self.navigator(query, download_path, saveas, print_list, p, url_selected = url_selected)
					#if url_selected:
						#url_selected = self.url + url_selected[1:]
						#data_files_tree_sub, data_dict_sub, data_dict_name_sub = self.print_tree_files(url_selected, print_list = True, level = level_sub)
						#debug(data_dict_sub = data_dict_sub)						
						
				return self.navigator(query, download_path, saveas, print_list, None, data, data_files_tree)
		elif p[0].lower() == 's' or 's=' in p.lower():
			if p[0] == 's':
				query = p[1:].lower()
			elif p[:2].lower() == 's=':
				query = p[2:].lower()
			return self.navigator(query, download_path, saveas, True)
		return self.navigator(None, download_path, saveas, True)
	
	def usage(self):
		debug("USAGE")
		parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
		parser.add_argument('QUERY', help = unquote("Search for or project url file, example: https://sourceforge.net/projects/taskswitchxp/files/TaskSwitchXP%20Pro%202.x/2.0.11/TaskSwitchXP_2.0.11.exe/download"), action = 'store')
		parser.add_argument('-p', '--download-path', help = 'Save download to', action = 'store')
		parser.add_argument('-o', '--saveas', help = 'Save download file as other name', action = 'store')
		parser.add_argument('-l', '--level', help = 'Level of trees file viewer', action = 'store', type = int, default = 1)
		parser.add_argument('-c', '--copy-url', help = 'Copy download url generated', action = 'store_true')
		parser.add_argument('-d', '--download', help = 'Download url generated', action = 'store_true')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.QUERY == 'c':
				args.QUERY = clipboard.paste()
				print(make_colors("QUERY:", 'lw', 'lr') + " " + make_colors(args.QUERY, 'b', 'ly'))
			if 'https://' in args.QUERY or 'http://' in args.QUERY:
				if len(re.split("/", args.QUERY)) == 5:
					self.download_latest(args.QUERY, args.download_path, args.saveas, clip = args.copy_url, downloadit = args.download)
				else:
					self.download(args.QUERY, args.download_path, args.saveas, clip = args.copy_url, downloadit = args.download)
			else:
				self.navigator(args.QUERY, args.download_path, args.saveas, level = args.level)
		
if __name__ == '__main__':
	c = sourceforge()
	c.usage()
	#c.print_tree_files("https://sourceforge.net/projects/libtorrent/files/py-libtorrent/")
	#c.get_files("https://sourceforge.net/projects/libtorrent/files/py-libtorrent/")
	#c.download("https://sourceforge.net/projects/libtorrent/files/py-libtorrent/python-libtorrent-1.0.3.win32.msi/")
	#  c.download("https://sourceforge.net/projects/taskswitchxp/files/TaskSwitchXP%20Pro%202.x/2.0.11/TaskSwitchXP_2.0.11.exe/download")
	#c.search(sys.argv[1])
	#c.navigator(sys.argv[1])
	
	#c.details('https://sourceforge.net/projects/ubuntudde/')
	