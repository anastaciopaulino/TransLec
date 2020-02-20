# -*- coding: utf-8 -*-
from googletrans import Translator
import os

translator = Translator()
count = 0

class Trans:
	def __init__(self, filename):
		# -*- O unicode não é necessário para mostrar só o texto -*-
		self.name = filename
		self.send = open(self.name,'r') 
		self.responso = open("pt-"+self.name,'w')

		for line in self.send.readlines():   
			self.traduzido = translator.translate(line, dest='pt').text
			self.responso.write(self.traduzido+'\n')

		# -*- Closing -*-
		self.send.close()
		self.responso.close()
files = []
class Path:
    def __init__(self, path="."):
        self.path = os.listdir(path)
        self.dir = self.path
        for file in self.dir:
            if(os.path.isfile(file)):
                if (".srt" in file) or (".vtt" in file):
                    files.append(file)
                    print(f" {count} ADD ===> ", file)
Path()