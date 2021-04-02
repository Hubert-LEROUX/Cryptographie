"""
Bibliothèque d'outils commun de cryptographie
"""
import pandas as pd

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
STRING_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def resol_modulo(a,b, mod):
	"""
	Find c when a*c=b (modulo mod)
	:param a: number
	:param b: number
	:param mod: modulo
	:return: c
	"""
	for i in range(mod): # Pour tous les nombres du modulo
		if (a*i) % mod == b: # Si a*i modulo mod = b
			return i # Alors on a  trouvé ! On renvoit i
	return None


def desaccentueMessage(message):
	"""
	Cette fonction permet de dessacentuer un message et le mettre en majuscules
	"""
	m = message.upper().replace("É", "E").replace("À", "A").replace("Æ", "AE").replace("Ç", "C").replace("È", "E")
	m = m.replace("Œ", "OE").replace("Ù", "U").replace("Î", "I").replace("Ï", "I").replace("Ê", "E").replace("Ë", "E")
	m = m.replace("Ö", "O").replace("Ô", "O").replace("Â", "A").replace("Ä", "A")
	return m

def deponctuateMessage(message):
	m = ""
	for letter in desaccentueMessage(message):
		if letter in ALPHABET:
			m+=letter
	return m

def place_in_alphabet(letters):
	"""
	Affiche la place dans l'alphabet de chaque lettre A=1
	"""
	for l in letters:
		print(l, ':', str(ALPHABET.index(l)+1))


def aff_substitution(cipherAlphabet):
	# Ciphertext to plaintext
	print("Ciphertext :", STRING_ALPHABET)
	print("Plaintext  :", cipherAlphabet)
	# Plaintext to cipher text
	cip = ""
	for l in ALPHABET:
		if l in cipherAlphabet:
			cip += ALPHABET[cipherAlphabet.index(l)]
		else:
			cip += '*'
	print("Plaintext  :", STRING_ALPHABET)
	print("Ciphertext :", cip)


def substitution_dict_maker(plainAlphabet):
	"""
	Effectue un dictionnaire de substitution à partir le l'alphabet plaintext
	"""
	plainAlphabet = list(plainAlphabet)
	substitutionDict = dict()
	for i in range(len(ALPHABET)):
		substitutionDict[str(ALPHABET[i])] = plainAlphabet[i]
	return substitutionDict


def sommeMot(mot:str):
	"""
	Renvoie la somme d'un mot
	:param mot:
	:return:
	"""
	mot = desaccentueMessage(mot)
	somme = 0
	for l in mot:
		somme += ALPHABET.index(l)+1
	return somme


def pgcd(a,b):
	""" Description
	:type a:
	:param a:

	:type b:
	:param b:

	:raises:

	:rtype: 
	"""
	while b!=0:
		a, b = b, a % b
	return a


def ppcm(a, b):
    """ppcm(a,b): calcul du 'Plus Petit Commun Multiple' entre 2 nombres entiers a et b"""
    if (a == 0) or (b == 0):
        return 0
    else:
        return (a*b)//pgcd(a, b)


def reverse(texte):
	"""
	Reverse a text
	:param texte: text
	:return: reversed text
	"""
	result = ""
	for i in range(1, len(texte)+1):
		result += texte[-i]
	return result


def primeRelatives(a, b):
	"""

	:param a:
	:param b:
	:return: Si les deux nombres sont premiers entre eux
	"""
	if a != 0 and b != 0: # Si aucun des nombres n'est nul
		if ppcm(a,b) == a*b : # si le PPCM est différent de a*b
			return True
		return False
	return False


def txt2csv(filename:str, sep:str):
	""" 
	Convertis un fichier texte en un fichier csv
	:type filename: string 
	:param filename: Nom du fichier sans l'extension

	:type sep: String
	:param sep: Séparateur CSV

	:raises: 

	:rtype: ø
	"""
	with open(filename+'.txt', 'r', newline='') as fich_i:
		initial = pd.read_csv(fich_i, delimiter=sep)
	initial.to_csv(filename+'.csv', index=False, sep=';')

def prettifyCiphertext(ciphertext, chunksize=5):
	prettifiedCiphertext = ""
	for indiceLetter in range(len(ciphertext)):
		prettifiedCiphertext += ciphertext[indiceLetter]
		if (indiceLetter + 1)%chunksize ==0:
			prettifiedCiphertext +=" "
	return prettifiedCiphertext

def columnarTansposition_keyWord2key(keyword, first=0):
	""" This function calculate the index of the rows defined by a keyword which is given
	:type keyword:
	:param keyword: keyword given to rearrange the colums	

	:raises:

	:rtype: list of integrers
	"""
	key = list(range(first, len(keyword)+first))
	keywordWithIndexes = [(keyword[i], i) for i in range(len(keyword))]
	keywordWithIndexes.sort(key=lambda x: x[0])
	keywordWithIndexes = [(keywordWithIndexes[i][0], keywordWithIndexes[i][1], i+first) for i in range(len(keyword))]
	keywordWithIndexes.sort(key=lambda x: x[1])
	key = [x[2] for x in keywordWithIndexes]
	return key
	
def columnarTansposition_makeRectangleWithPlaintext_withkeyword(plaintext, keyword):
	""" Generate a rectangle of transposition
	:type plaintext:
	:param plaintext: plaintext to encipher

	:type keyword:
	:param keyword: keyword for the columns

	:raises:

	:rtype: ciphertext
	"""
	key = columnarTansposition_keyWord2key(keyword, first=1)
	print(" ".join(list(keyword)))
	return columnarTansposition_makeRectangleWithPlaintext_withkey(plaintext, key)

	
def columnarTansposition_makeRectangleWithPlaintext_withkey(plaintext, key):
	""" Generate a rectangle of transposition with the key consistinh of integrers
	:type plaintext:
	:param plaintext: plaintext to encipher

	:type key:
	:param key: keyword for the columns

	:raises:

	:rtype: ciphertext
	"""
	plaintext = deponctuateMessage(plaintext) # On purge le texte
	rectangleWidth = len(key) # On trouve la largeur du rectangle
	rectangleHeight = len(plaintext)//rectangleWidth # Nombre de lignes pleines
	rectangleLastRowWidth = len(plaintext) % rectangleWidth # Le reste de lettres à caser dans la dernière ligne
	ciphertext = "" # on initialise le texte chiffré
	columns = [[] for _ in range(rectangleWidth)]# On crée une liste 2D qui va stocker les colonnes
	print(" ".join([str(x) for x in key]))
	print("="*(2*rectangleWidth-1))
	for rowIndice in range(rectangleHeight):
		for columnIndice in range(rectangleWidth):
			letter = plaintext[rowIndice*rectangleWidth+columnIndice] # on trouve la lettre
			columns[key[columnIndice]-1].append(letter) # On ajoute la lettre à la liste 2D
			print(letter, end=" ") # On affiche la lettre
		print()
	for i in range(rectangleLastRowWidth):
		letter = plaintext[rectangleHeight*rectangleWidth+i] # on trouve la lettre
		columns[key[i]-1].append(letter) # On ajoute la lettre à la liste 2D
		print(letter, end=" ") # On affiche la lettre
	print()
	ciphertext = prettifyCiphertext("".join(["".join(column)  for column in columns]), 5)
	return ciphertext

def columnarTransposition_makeRectangleWithCiphertext_withkeyword(ciphertext, keyword):
	key = columnarTansposition_keyWord2key(keyword)
	return columnarTransposition_makeRectangleWithCiphertext_withkey(ciphertext, key)

def columnarTransposition_makeRectangleWithCiphertext_withkey(ciphertext, key):
	ciphertext = deponctuateMessage(ciphertext) # On purge le texte donné
	rectangleWidth = len(key) # On trouve la largeur du rectangle
	rectangleHeight = len(ciphertext)//rectangleWidth # Nombre de lignes pleines
	rectangleLastRowWidth = len(ciphertext) % rectangleWidth # Le reste de lettres à caser dans la dernière ligne
	plaintext = "" # On initialise la chaîne de caractères plaintext
	columns = [[] for _ in range(rectangleWidth)]
	# print(rectangleWidth, rectangleHeight)
	for columnIndex in range(rectangleWidth):# Pour chaque colonne
		for letter in ciphertext[columnIndex*rectangleHeight:(columnIndex+1)*rectangleHeight]: # Pour chaque lettre de la colonne
			columns[key.index(columnIndex)].append(letter) #Les insérer
	# print(columns)
	rows = [["#"]*rectangleWidth for _ in range(rectangleHeight)] # Initialise une liste 2D des lignes
	# print(rows)
	for columnIndex in range(rectangleWidth):
		for rowIndex in range(rectangleHeight):
			rows[rowIndex][columnIndex] = columns[columnIndex][rowIndex]
	# print(rows)
	for row in rows:
		for letter in row:
			plaintext+=letter
	return prettifyCiphertext(plaintext)

Messages = ["HDUCP IEATL EIEUU OENOI XMMCI TATDF DSSHC HSSVS ISTAO TRNGO HRSSG OHASF EMBLH FPEEO EE", "ECDTM ECAER AUOOL EDSAM MERNE NASSO DYTNR VBNLC RLTIQ LAETR IGAWE BAAEI HOR", "LASER BEAMS CAN BE MODULATED TO CARRY MORE INTELLIGENCE THAN RADIO WAVESQR", "TNGTH CYIIL XHEIH PANCA AXHGR OUFOA EMITE LSOIP INDSR ROEAR ERANX EEEFT IUISE AEANS CESON EX"]

print(columnarTransposition_makeRectangleWithCiphertext_withkeyword(Messages[0], "CREAMPUFF"))
