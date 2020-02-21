# -*- coding: utf-8 -*-
from googletrans import Translator
import os

translator = Translator()
files = []
count = 0

class Trans:
	def __init__(self, filename, dest):
		# -*- O unicode não é necessário para mostrar só o texto -*-
		self.name = filename
		self.send = open(self.name,'r') 
		self.responso = open("pt-"+self.name,'w')

		for line in self.send.readlines():   
			self.traduzido = translator.translate(line, dest=dest).text
			self.responso.write(self.traduzido+'\n')

		# -*- Closing -*-
		self.send.close()
		self.responso.close()
class Transp:
	def __init__(self, phrase, dest):
		out = translator.translate(phrase, dest=dest).text
		print("Out: ", out)

class Path:
	def __init__(self, path="."):
		self.path = os.listdir(path)
		self.dir = self.path
		for file in self.dir:
			if(os.path.isfile(file)):
				if ((".srt" in file) or (".vtt" in file)):
					files.append(file)
	def printlist():
		os.system('''
white="\033[1;37m"                                          
grey="\033[0;37m"                                           
purple="\033[0;35m"                                         
red="\033[1;31m"                                            
green="\033[1;32m"                                          
yellow="\033[1;33m"                                         
purple="\033[0;35m"                                         
cyan="\033[0;36m"                                           
cafe="\033[0;33m"                                           
fiuscha="\033[0;35m"                                        
blue="\033[1;34m"                                           
nc="\e[0m"
printf "
╔═══════════════════════════════════════════════════════════════════════════════════╗
║[+]By: Anastácio Paulino:                                                          ║
║ ┖[+] A Legião The Hackers Security                                                ║
╚═══║═══════════════════════════════════════════════════════════════════════════════╝
╔══[+]═══════════════════════════════════════════════════════════════╗
║   ┖[+]Listing:                                                     ╚═══════════════
║     ┖[+]                                                                      
║      [+]           Name                                    Size                                             
║      [+]  ------------------------                       ---------                                              "''')
		for file in files:
			print("\n║      [+]   {:45} {}".format(file, os.stat(file).st_size))
		print("""
║                                                                    ╔═══════════════
╚════════════════════════════════════════════════════════════════════╝\n""")