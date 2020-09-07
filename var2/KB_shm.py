# -*- coding: utf-8 -*-
"""
Copyright 2014 Brno University of Technology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# Příklad načtení:
'''
from KB_shm import *
'''

import os
import re
from ctypes import CDLL, c_char, c_char_p, c_int, c_uint, c_void_p, POINTER
#from ctypes import byref

import collections
from orderedset import OrderedSet

# Pro debugování:
import inspect
DEBUG_EN = True
DEBUG_EN = False
#

def print_dbg(text=""):
	if not DEBUG_EN:
		return
	callerframerecord = inspect.stack()[1]
	frame = callerframerecord[0]
	info = inspect.getframeinfo(frame)
	
	head = "("+ info.filename +", "+ info.function +", "+ str(info.lineno) +")"
	
	print( head +":\n'''\n"+ text +"\n'''" )
#

# Získání absolutní cesty k adresáři ve kterém je tento soubor.
script_dir = os.path.dirname(os.path.abspath(__file__))
# Načtení dynamické knihovny "libKB_shm.so"
libKB_shm = CDLL( os.path.join(script_dir, "libKB_shm.so") )

# Pro jazyky C/C++
'''
KB_shm_p = c_void_p(0)
KB_shm_fd = c_int(-1)
status = c_int(0)

status = c_int( connectKBSharedMem( byref(KB_shm_p), byref(KB_shm_fd) ) )
if status.value != 0:
	print("ERROR")
	exit(1)

. . .

status = c_int( disconnectKBSharedMem( byref(KB_shm_p), byref(KB_shm_fd) ) )
if status.value != 0:
	print("ERROR")
	exit(1)

exit(0)
'''
connectKBSharedMem = libKB_shm.connectKBSharedMem
connectKBSharedMem.argtypes = [POINTER(c_void_p), POINTER(c_int)]
connectKBSharedMem.restype = c_int

disconnectKBSharedMem = libKB_shm.disconnectKBSharedMem
disconnectKBSharedMem.argtypes = [POINTER(c_void_p), POINTER(c_int)]
disconnectKBSharedMem.restype = c_int

# Pro jazyky Java, Python, ...
'''
KB_shm_p = c_void_p(0)
KB_shm_fd = c_int(-1)
status = c_int(0)

KB_shm_fd = c_int( connectKB_shm() )
if KB_shm_fd.value < 0:
	print("ERROR")
	exit(1)

KB_shm_p = c_void_p( mmapKB_shm(KB_shm_fd) )
if KB_shm_p.value == None:
	print("ERROR")
	disconnectKB_shm(KB_shm_p, KB_shm_fd)
	exit(1)

. . .

status = c_int( disconnectKB_shm(KB_shm_p, KB_shm_fd) )
if status.value != 0:
	print("ERROR")
	exit(1)

KB_shm_p = c_void_p(0)
KB_shm_fd = c_int(-1)
exit(0)
'''
checkKB_shm = libKB_shm.checkKB_shm
checkKB_shm.argtypes = [c_char_p]
checkKB_shm.restype = c_int

connectKB_shm = libKB_shm.connectKB_shm
connectKB_shm.argtypes = [c_char_p]
connectKB_shm.restype = c_int

mmapKB_shm = libKB_shm.mmapKB_shm
mmapKB_shm.argtypes = [c_int]
mmapKB_shm.restype = c_void_p

disconnectKB_shm = libKB_shm.disconnectKB_shm
disconnectKB_shm.argtypes = [c_void_p, c_int]
disconnectKB_shm.restype = c_int

# Funkce pro získání řetězců
'''
KBSharedMemDataAt( KB_shm_p, 1, 1 )
c_char_p( KBSharedMemDataAt( KB_shm_p, 1, 1 ) )
print( c_char_p( KBSharedMemDataAt( KB_shm_p, 1, 1 ) ).value )

print( c_char_p( KBSharedMemHeadFor( KB_shm_p, 'p', 1 ) ).value )
print( c_char_p( KBSharedMemHeadFor_Boost( KB_shm_p, 'p', 1, byref(line) ) ).value )
'''
KBSharedMemHeadAt = libKB_shm.KBSharedMemHeadAt
KBSharedMemHeadAt.argtypes = [c_void_p, c_uint, c_uint]
KBSharedMemHeadAt.restype = c_void_p

KBSharedMemHeadFor = libKB_shm.KBSharedMemHeadFor
KBSharedMemHeadFor.argtypes = [c_void_p, c_char, c_uint]
KBSharedMemHeadFor.restype = c_void_p

KBSharedMemHeadFor_Boost = libKB_shm.KBSharedMemHeadFor_Boost
KBSharedMemHeadFor_Boost.argtypes = [c_void_p, c_char, c_uint, POINTER(c_uint)]
KBSharedMemHeadFor_Boost.restype = c_void_p

KBSharedMemDataAt = libKB_shm.KBSharedMemDataAt
KBSharedMemDataAt.argtypes = [c_void_p, c_uint, c_uint]
KBSharedMemDataAt.restype = c_void_p

# Funkce pro získání verze

KBSharedMemVersion = libKB_shm.KBSharedMemVersion
KBSharedMemVersion.argtypes = [c_void_p]
KBSharedMemVersion.restype = c_char_p

getVersionFromSrc = libKB_shm.getVersionFromSrc
getVersionFromSrc.argtypes = [c_char_p]
getVersionFromSrc.restype = c_char_p

getVersionFromBin = libKB_shm.getVersionFromBin
getVersionFromBin.argtypes = [c_char_p]
getVersionFromBin.restype = c_char_p

# Příklad použití:
'''
KB_shm_p = c_void_p(0)
KB_shm_fd = c_int(-1)
status = c_int(0)

KB_shm_fd = c_int( connectKB_shm() )
if KB_shm_fd.value < 0:
	print("ERROR")
	exit(1)

KB_shm_p = c_void_p( mmapKB_shm(KB_shm_fd) )
if KB_shm_p.value == None:
	print("ERROR")
	disconnectKB_shm(KB_shm_p, KB_shm_fd)
	exit(1)

#. . .#

raw_input("hit enter...")

str = c_char_p( KBSharedMemHeadAt( KB_shm_p, 1, 1 ) ).value
i = 1
while str != None:
	j = 1
	while str != None:
		print(str)
		j += 1
		str = c_char_p( KBSharedMemHeadAt( KB_shm_p, i, j ) ).value
	i += 1
	str = c_char_p( KBSharedMemHeadAt( KB_shm_p, i, 1 ) ).value

raw_input("hit enter...")

j = 1
str = c_char_p( KBSharedMemHeadFor( KB_shm_p, 'p', j ) ).value
while str != None:
	print(str)
	j += 1
	str = c_char_p( KBSharedMemHeadFor( KB_shm_p, 'p', j ) ).value

raw_input("hit enter...")

str = c_char_p( KBSharedMemDataAt( KB_shm_p, 1, 1 ) ).value
i = 1
while str != None:
	j = 1
	while str != None:
		print(str)
		j += 1
		str = c_char_p( KBSharedMemDataAt( KB_shm_p, i, j ) ).value
	i += 1
	str = c_char_p( KBSharedMemDataAt( KB_shm_p, i, 1 ) ).value

raw_input("hit enter...")

#. . .#

status = c_int( disconnectKB_shm(KB_shm_p, KB_shm_fd) )
if status.value != 0:
	print("ERROR")
	exit(1)

KB_shm_p = c_void_p(0)
KB_shm_fd = c_int(-1)
exit(0)
'''

class KbShmException(Exception):
	pass
#

class DataTypeSet(OrderedSet):
	def __str__(self):
		return "+".join(data_supertype for data_supertype in self if not data_supertype.startswith("__"))

class KB_shm(object):
	'''
	Třída zastřešující KB_shm.
	'''
	
	DataTypeSet = DataTypeSet
	KbHeadColumn = collections.namedtuple("KbHeadColumn", "type flags prefix name")
	
	def __init__(self, kb_shm_name=None, multivalue_delim="|"):
		'''
		Inicializace.
		'''
		if isinstance(kb_shm_name, str):
			kb_shm_name = kb_shm_name.encode()
		
		self.KB_shm_p = c_void_p(0)
		self.KB_shm_fd = c_int(-1)
		self.KB_shm_name = c_char_p(kb_shm_name)
		self.headLine_Boost = {} # Slovník TYPE:LINE(Číslo řádku na kterém je daný typ definován)
		self.headCol_Boost = {} # Slovník LINE:{COLUMN_NAME:COLUMN}
		self.headColCnt_Boost = {} # Slovník LINE:COLUMN_COUNT(Počet sloupců na daném řádku)
		self.headType_Boost = {} # Slovník LINE:TYPE
		self.typeSet_Buffer = {} # Slovník repr(ENTITY_TYPE_SET):{COLUMN_NAME:[(COLUMN, TYPE), ...]} -- buffer pro určení sloupce pro konkrétní uspořádanou množinu typů
		self.typeSet_Buffer_max = 100 # Maximální velikost bufferu self.typeSet_Buffer
		self.typeSet_Buffer_fifo = [] # FIFO fronta bufferu self.typeSet_Buffer
		self.multivalue_delim = multivalue_delim
		self.type_delim = "+"
		
		self.data_type_col = None # Sloupec ve kterém je definován typ entity
		
		self._alive = False
		self._prepared = False
		
		# viz https://knot.fit.vutbr.cz/wiki/index.php/Decipher_ner#Sloupce_v_HEAD-KB
		self.HEAD_COLUMN_PARSER = re.compile(r"""(?ux)
			^
			(?:<(?P<TYPE>[^>]+)>)?
			(?:\{(?P<FLAGS>(?:\w|[ ])*)(?:\[(?P<PREFIX_OF_VALUE>[^\]]+)\])?\})?
			(?P<NAME>(?:\w|[ ])+)?
			$
		""")
	
	def start(self, kb_shm_name=None):
		'''
		Připojí sdílenou paměť.
		'''
		assert not self._alive
		
		if kb_shm_name == None:
			kb_shm_name = self.KB_shm_name
		else:
			kb_shm_name = c_char_p(kb_shm_name)
		
		self.KB_shm_fd = c_int( connectKB_shm(kb_shm_name) )
		if self.KB_shm_fd.value < 0:
			raise KbShmException("connectKB_shm")
		
		self.KB_shm_p = c_void_p( mmapKB_shm(self.KB_shm_fd) )
		if self.KB_shm_p.value == None:
			disconnectKB_shm(self.KB_shm_p, self.KB_shm_fd)
			raise KbShmException("mmapKB_shm")
		
		self._alive = True
		
		self.prepareBoosts()
	
	def end(self):
		'''
		Odpojí sdílenou paměť.
		'''
		if self.KB_shm_fd.value != -1:
			status = c_int(0)
			status = c_int( disconnectKB_shm(self.KB_shm_p, self.KB_shm_fd) )
			if status.value != 0:
				raise KbShmException("disconnectKB_shm")
		
		self.__init__(self.KB_shm_name.value, self.multivalue_delim)
	
	def check(self, kb_shm_name=None):
		'''
		Zkontroluje zda je sdílená paměť k dispozici.
		'''
		if kb_shm_name == None:
			kb_shm_name = self.KB_shm_name
		else:
			kb_shm_name = c_char_p(kb_shm_name)
		
		status = c_int(0)
		status = c_int( checkKB_shm(kb_shm_name) )
		if status.value != 0:
			return False
		else:
			return True
	
	def prepareBoosts(self):
		assert self._alive
		
		self.headLine_Boost = {}
		self.headType_Boost = {}
		self.headCol_Boost = {}
		
		for line_number, line_content in self.iterKbHead():
			column_counter = 0
			for column_number, column_content in line_content:
				column_counter = column_number
				column_name = column_content.name
				if column_number == 1:
					head_type = column_content.type
					if head_type is None:
						raise KbShmException("prepareBoosts: Bad syntax of HEAD-KB!")
					self.headLine_Boost[head_type] = line_number
					self.headType_Boost[line_number] = head_type
					self.headCol_Boost[line_number] = {}
					print_dbg("%s: %s" % (head_type, line_number))
					
					if not column_name:
						column_counter = 0
						if next(line_content, None) is not None:
							raise KbShmException("prepareBoosts: Bad syntax of HEAD-KB!")
						break
				else:
					if not column_name:
						raise KbShmException("prepareBoosts: Empty name of column %s at line %s in HEAD-KB!" % (column_number, line_number))
				
				self.headCol_Boost[line_number][column_name] = column_number
				print_dbg("%s, %s: %s" % (line_number, column_name, column_number))
				
				if column_name == "TYPE":
					if self.data_type_col is None:
						self.data_type_col = column_number
					elif self.data_type_col != column_number:
						raise KbShmException("prepareBoosts: Attribute TYPE must be at same column for each type of entity in HEAD-KB!")
			
			self.headColCnt_Boost[line_number] = column_counter
		
		if self.data_type_col is None:
			raise KbShmException("prepareBoosts: There is no TYPE column in HEAD-KB!")
		
		self._prepared = True
	
	def version(self):
		assert self._alive
		
		result = c_char_p( KBSharedMemVersion( self.KB_shm_p ) ).value
		if isinstance(result, bytes):
			result = result.decode()
		else:
			raise KbShmException("KBSharedMemVersion: None")
		
		return result
	
	def headAt(self, line, col):
		assert self._alive
		assert isinstance(line, int)
		assert isinstance(col, int)
		
		result = c_char_p( KBSharedMemHeadAt( self.KB_shm_p, line, col ) ).value
		if result is not None:
			result = result.decode()
			splitted = self.HEAD_COLUMN_PARSER.search(result)
			try:
				result = self.KbHeadColumn(splitted.group("TYPE"), splitted.group("FLAGS"), splitted.group("PREFIX_OF_VALUE"), splitted.group("NAME"))
			except AttributeError:
				if splitted is None:
					raise KbShmException("Bad syntax of HEAD-KB!")
				else:
					raise
		return result
	
	def iterKbHeadLine(self, line):
		column = 1
		while True:
			column_content = self.headAt(line, column)
			if column_content is None:
				break
			
			yield column, column_content
			column += 1
	
	def iterKbHead(self):
		line = 1
		while True:
			column_content = self.headAt(line, 1)
			if column_content is None:
				break
			
			yield line, self.iterKbHeadLine(line)
			line += 1
	
	def headExist(self, ent_type_set):
		'''
		headExist(OrderedSet(["__generic__", "person", "__stats__"]))
		
		@param ent_type_set
			Uspořádaná množina typů, kterých daná entita podtypem.
		@return
			Pokud jsou definovány všechny typy z \a ent_type_set, pak vrátí True, jinak False.
		'''
		assert self._alive
		assert isinstance(ent_type_set, OrderedSet)
		
		if all(self.headLine(t) != None for t in ent_type_set):
			result = True
		else:
			result = False
		return result
	
	def headLine(self, ent_supertype):
		'''
		headLine("person")
		
		@param ent_supertype
			Název nadtypu entity.
		@return
			Vrátí číslo řádku na kterém je definován typ \a ent_supertype. Dojde-li k chybě, vrátí None.
		'''
		assert self._alive and self._prepared
		assert isinstance(ent_supertype, str)
		
		if ent_supertype in self.headLine_Boost:
			result = self.headLine_Boost[ent_supertype]
		else:
			result = None
		return result
	
	def headFor(self, ent_type_set, col):
		'''
		headFor(OrderedSet(["__generic__", "person", "__stats__"]), 9)
		
		Pro uspořádanou množinu typů \a ent_type_set vrátí definici \a col-tého sloupce.
		
		@param ent_type_set
			Uspořádaná množina typů, kterých daná entita podtypem.
		@param col
			Sloupec, jehož definici chceme zjistit.
		@return
			Vrátí definici \a col-tého sloupce. Dojde-li k chybě, vrátí None.
		'''
		assert self._alive and self._prepared
		assert isinstance(ent_type_set, OrderedSet)
		
		colCnt = 0
		resultCol = None
		line = None
		for ent_supertype in ent_type_set:
			line = self.headLine(ent_supertype)
			if line == None:
				return None
			
			if col <= (colCnt + self.headColCnt_Boost[line]):
				resultCol = col - colCnt
				break
			else:
				colCnt += self.headColCnt_Boost[line]
		
		if line and resultCol:
			result = self.headAt(line, resultCol)
		else:
			result = None
		return result
	
	def headCol(self, ent_type_set, col_name, col_name_type=None):
		'''
		headCol(OrderedSet(["__generic__", "person", "__stats__"]), "DATE OF BIRTH")
		headCol(OrderedSet(["__generic__", "person", "__stats__"]), "DATE OF BIRTH", "person")
		
		Pro typ \a ent_type_set vrátí číslo sloupce \a col_name.
		
		@param ent_type_set
			Uspořádaná množina typů, kterých daná entita podtypem.
		@param col_name
			Název sloupce, jehož číslo chceme zjistit.
		@param col_name_type
			Specifikace typu, ve kterém bude hledán \a col_name.
		@return
			Vrátí číslo sloupce \a col_name. Dojde-li k chybě, vrátí None.
		'''
		assert self._alive and self._prepared
		
		return self._headColBuffered(ent_type_set, col_name, col_name_type)
	
	def _headCol(self, ent_type_set, col_name, col_name_type=None):
		assert self._alive and self._prepared
		
		def _headLineAndCol(self, ent_supertype, col_name):
			line = self.headLine(ent_supertype)
			if line:
				if col_name in self.headCol_Boost[line]:
					col = self.headCol_Boost[line][col_name]
				else:
					col = None
			else:
				col = None
			return line, col
		#
		
		col = 0
		colCnt = 0
		line = None
		if col_name_type: # Je-li definován \a col_name_type, hledá se \a col_name pouze v něm.
			if col_name_type not in ent_type_set:
				return None
			
			for ent_supertype in ent_type_set:
				if ent_supertype == col_name_type:
					line, col = _headLineAndCol(self, ent_supertype, col_name)
					return (col and col + colCnt)
				else:
					line = self.headLine(ent_supertype)
					colCnt += self.headColCnt_Boost[line]
			return None
		else: # Není-li definován \a col_name_type, pak se postupně projde celá uspořádaná množina typů \a ent_type_set, kterých je daná entita podtypem.
			for ent_supertype in ent_type_set:
				line, col = _headLineAndCol(self, ent_supertype, col_name)
				if col:
					col += colCnt
					return col
				else:
					if line == None:
						return None # NOTE: Vyhodit chybovou hlášku? "None" znamená chybu, jinak OK.
					colCnt += self.headColCnt_Boost[line]
		
		return None
	
	def _headColBuffered(self, ent_type_set, col_name, col_name_type=None):
		assert self._alive and self._prepared
		# využívá self.typeSet_Buffer - Slovník repr(ENTITY_TYPE_SET):{COLUMN_NAME:[(COLUMN, TYPE), ...]}
		
		ent_type_set_index = repr(ent_type_set)
		
		# není-li typ entity v bufferu, natáhni jej
		if ent_type_set_index not in self.typeSet_Buffer:
			colCnt = 0
			column_names = {}
			for ent_supertype in ent_type_set:
				line = self.headLine(ent_supertype)
				if line:
					for c_name in self.headCol_Boost[line]:
						c = self.headCol_Boost[line][c_name]
						column_names.setdefault(c_name, []).append((c + colCnt, ent_supertype))
					colCnt += self.headColCnt_Boost[line]
				else:
					return None
			if self.typeSet_Buffer_max > 0 and len(self.typeSet_Buffer_fifo) >= self.typeSet_Buffer_max:
				old_item = self.typeSet_Buffer_fifo.pop(0)
				self.typeSet_Buffer.pop(old_item)
			self.typeSet_Buffer[ent_type_set_index] = column_names
			self.typeSet_Buffer_fifo.append(column_names)
			assert len(self.typeSet_Buffer) == len(self.typeSet_Buffer_fifo)
		
		# vrať číslo požadovaného sloupce
		if col_name in self.typeSet_Buffer[ent_type_set_index]:
			columns = self.typeSet_Buffer[ent_type_set_index][col_name]
			if col_name_type:
				if col_name_type in ent_type_set:
					for c, t in columns:
						if t == col_name_type:
							col = c
							break
					else:
						return None
				else:
					return None
			else:
				col = columns[0][0]
		else:
			return None
		
		return col
	
	def headType(self, line):
		assert self._alive and self._prepared
		
		if line in self.headType_Boost:
			return self.headType_Boost[line]
		else:
			return None
	
	def dataAt(self, line, col):
		assert self._alive
		
		result = c_char_p( KBSharedMemDataAt( self.KB_shm_p, line, col ) ).value
		if isinstance(result, bytes):
			result = result.decode()
		
		return result
	
	def dataFor(self, line, col_name, col_name_type=None):
		'''
		dataFor(10000, "DATE OF BIRTH", col_name_type="person")
		'''
		assert self._alive
		
		ent_type_set = self.dataType(line)
		if ent_type_set == None:
			return None
		
		col = self.headCol(ent_type_set, col_name, col_name_type)
		if col == None:
			return None
		
		return self.dataAt(line, col)
	
	def dataType(self, line):
		assert self._alive and self._prepared
		
		data_type = self.dataAt(line, self.data_type_col)
		try:
			data_type = data_type.split(self.type_delim)
		except AttributeError:
			if data_type is None:
				raise KbShmException("Line %s does not have column %s" % (line, self.data_type_col))
			else:
				raise
		data_type_set = DataTypeSet(data_type)
		
		if "__generic__" in self.headLine_Boost and "__generic__" not in data_type_set:
			data_type_set = ["__generic__"] | data_type_set
		if "__stats__" in self.headLine_Boost and "__stats__" not in data_type_set:
			data_type_set = data_type_set | ["__stats__"]
		
		return data_type_set
	
	@staticmethod
	def getVersionFromSrc(kb_path):
		assert isinstance(kb_path, str)
		
		kb_path = c_char_p(kb_path.encode())
		
		result = c_char_p( getVersionFromSrc(kb_path) ).value
		if isinstance(result, bytes):
			result = result.decode()
		else:
			raise KbShmException("getVersionFromSrc: None")
		
		return result
	
	@staticmethod
	def getVersionFromBin(kb_bin_path):
		assert isinstance(kb_bin_path, str)
		
		kb_bin_path = c_char_p(kb_bin_path)
		
		result = c_char_p( getVersionFromBin(kb_bin_path) ).value
		if isinstance(result, bytes):
			result = result.decode()
		else:
			raise KbShmException("getVersionFromBin: None")
		
		return result
#

# konec souboru KB_shm.py
