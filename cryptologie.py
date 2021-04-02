import pandas as pd
import numpy as np

from commonTools import desaccentueMessage, ALPHABET, STRING_ALPHABET, deponctuateMessage, prettifyCiphertext, place_in_alphabet, resol_modulo


def affineEncipher(plaintext, a, b=0):
	"""
	Encipher a plaintext by affine encryption	C = aP + b
	:param a: Multiplicative facteur
	:param b: Additive facteur
	:param plaintext: Plaintext
	:return: ciphertext
	"""
	ciphertext = "" # Ciphertext
	for l in plaintext.upper(): # Pour chaque lettre dans le plaintext
		if l in ALPHABET: # Si la lettre se trouve dans l'alphabet..
			x = ALPHABET.index(l) + 1 # ... On trouve son index
			# print(x, end=' | ') # DEBUGGING HELP
			cipher_letter = ALPHABET[(a*x + b-1) % 26] # On la chiffre
			# print('number: ', (a*x + b) % 25, end=' | ') # DEBUGGING HELP
			# print(cipher_letter) # DEBUGGING HELP
			ciphertext += cipher_letter # On l'ajoute au texte
		else: # Sinon
			ciphertext += l # On ajoute la lettre/le caractère tel quel
	return ciphertext


def reduceNumberOfRowsOfCsvFile(inputFilename:str, outputFilename:str, maximumNumberOfRows=100):
	"""[Reduces the number of rows of a csv file]

	Arguments:
		inputFilename {[string]} -- [Path of the file who is too big]
		outputFilename {[string]} -- [Path of the new file which will be smaller]

	Keyword Arguments:
		maximumNumberOfRows {int} -- [maximum of Number of rows to take from the first file] (default: {100})
	"""	
	with open(inputFilename, 'r', newline='') as fich: # On ouvre le fichier d'entrée
		df = pd.read_csv(fich, delimiter=' ', nrows=maximumNumberOfRows) # On ne prend qu'un certain nombre de lignes, 100 par défaut
	df.to_csv(outputFilename, index=False, sep=';') # On enregistre le dataframe obtenu


def CesarCodeDecipher(ciphertext):
	"""
	Decipher a cesar ciphertext
	:param ciphertext:
	:return: plaintext
	"""
	ciphertext = ciphertext.split(',')
	result = ''
	alpha = list(ALPHABET*2)
	for decalage in range(3, 4):
		for carac in ciphertext:
			result += alpha[eval(carac)+decalage]
		# print(result)
		# result = ''
	return result


def lecture_complexe(enciphertext):
	"""
	Tente de résoudre un anagramme
	:param enciphertext: texte chiffré
	:return: solution
	"""
	mots = enciphertext.split(' ')
	print(mots)
	result = ''
	for dec in range(1, 5):
		for mot in mots:
			mot = list(mot)
			result += mot[dec]
	return result


def transposition(ciphertext, a, b):
	"""
	Lit les mots du ciphertext dans un ordre particulier
	:param ciphertext:
	:param a: écart entre chaque mot
	:return: plaintext
	"""
	mots_mel = ciphertext.split(" ")
	plaintext = ''
	for i in range(len(mots_mel)):
		plaintext += mots_mel[((i*a + b) % len(mots_mel))]+' '
	# # TABLE
	# for column in range(a):
	# 	for row in range(len(mots_mel)//a+1):
	# 		plaintext += mots_mel[(row*a +column) % len(mots_mel)] + " "
	return plaintext


def affineDecipher(ciphertext:str, a, b=0):
	"""
	Decipher a ciphertext crypted by an affine method
	C = a * P + b
	:param ciphertext: it is a string of the crypted text
	:param a: Number 
	:param b: Number
	:return: plaintext
	"""
	plaintext = ""
	cipherAlphabet = list(affineEncipher(''.join(ALPHABET), a, b)) # Création de l'alphaber de cipher
	for l in desaccentueMessage(ciphertext): # Pour chaque lettre dans le ciphertext
		if l in ALPHABET: # Si cette lettre appartient à l'alphabet, il faut la déchiffrer
			plaintextLetter = ALPHABET[cipherAlphabet.index(l)] # On déchiffre la lettre grâce à l'alphabet trouvé plus haut
			plaintext += plaintextLetter # On ajoute la lettre déchiffrée au message
		else: # Sinon, cette lettre est un chiffre ou une ponctuation
			plaintext += l # On l'ajoute comme tel au message déchiffré
	return plaintext # On retourne le message


def affine_alphabet(a,b=0):
	return list(affineEncipher(a, b, ''.join(ALPHABET)))


def message2Morse(message:str, reverse=False):
	"""
	Traduit un message en morse
	:param message: string du message à traduire
	:param reverse: est dacultatif et faux par défaut. Il permet d'inverser point et "-"
	"""
	message = desaccentueMessage(message)
	messageMorse = ""
	for lettre in message:
		if lettre == "A": messageMorse += ".-/"
		elif lettre == "B": messageMorse += "-.../"
		elif lettre == "C": messageMorse += "-.-./"
		elif lettre == "D": messageMorse += "-../"
		elif lettre == "E": messageMorse += "./"
		elif lettre == "F": messageMorse += "..-./"
		elif lettre == "G": messageMorse += "--./"
		elif lettre == "H": messageMorse += "..../"
		elif lettre == "I": messageMorse += "../"
		elif lettre == "J": messageMorse += ".---/"
		elif lettre == "K": messageMorse += "-.-/"
		elif lettre == "L": messageMorse += ".-../"
		elif lettre == "M": messageMorse += "--/"
		elif lettre == "N": messageMorse += "-./"
		elif lettre == "O": messageMorse += "---/"
		elif lettre == "P": messageMorse += ".--./"
		elif lettre == "Q": messageMorse += "--.-/"
		elif lettre == "R": messageMorse += ".-./"
		elif lettre == "S": messageMorse += ".../"
		elif lettre == "T": messageMorse += "-/"
		elif lettre == "U": messageMorse += "..-/"
		elif lettre == "V": messageMorse += "...-/"
		elif lettre == "W": messageMorse += ".--/"
		elif lettre == "X": messageMorse += "-..-/"
		elif lettre == "Y": messageMorse += "-.--/"
		elif lettre == "Z": messageMorse += "--../"
		elif lettre == ".": messageMorse += ".-.-.-/"
		elif lettre == ",": messageMorse += "--..--/"
		elif lettre == "?": messageMorse += "..--../"
		elif lettre == "/": messageMorse += "-..-./"
		elif lettre == "@": messageMorse += ".--.-./"
		elif lettre == "'": messageMorse += ".----./"
		elif lettre == "’": messageMorse += ".----./"
		elif lettre == "!": messageMorse += "-.-.--/"
		elif lettre == "(": messageMorse += "-.--./"
		elif lettre == ")": messageMorse += "-.--.-"
		elif lettre == "&": messageMorse += ".-.../"
		elif lettre == ":": messageMorse += "---.../"
		elif lettre == ";": messageMorse += "-.-.-./"
		elif lettre == "=": messageMorse += "-...-/"
		elif lettre == "+": messageMorse += ".-.-./"
		elif lettre == "-": messageMorse += "-....-/"
		elif lettre == "_": messageMorse += "..--.-/"
		elif lettre == "\"": messageMorse += ".-..-./"
		elif lettre == "$": messageMorse += "...-..-/"
		elif lettre == "0": messageMorse += "-----/"
		elif lettre == "1": messageMorse += ".----/"
		elif lettre == "2": messageMorse += "..---/"
		elif lettre == "3": messageMorse += "...--/"
		elif lettre == "4": messageMorse += "....-/"
		elif lettre == "5": messageMorse += "...../"
		elif lettre == "6": messageMorse += "-..../"
		elif lettre == "7": messageMorse += "--.../"
		elif lettre == "8": messageMorse += "---../"
		elif lettre == "9": messageMorse += "----./"
		elif lettre == " ": messageMorse += "/"
		elif lettre == "\n": messageMorse += "\n"
		elif lettre == "\t": messageMorse += "\t"
		elif lettre == "\r": messageMorse += "\r"
		else: messageMorse+= "?/"
	if reverse: # On remplace les - par des . et inversement:
		messageMorseReversed = ""
		for caractere in messageMorse:
			if caractere == ".": messageMorseReversed += "-" # Le point devient une "-"
			elif caractere == "-": messageMorseReversed += "." # Le "-" devient un point
			else: messageMorseReversed += caractere
		return messageMorseReversed
	return messageMorse


def encipherSinglePolygraph(plaintextPolygraph, matrix, sizePolyGraph):
	#* On traduit le digraph grâce à la matrix
	ciphertextPolygraph = "" # On initialise le polygraph chiffré
	for row in range(sizePolyGraph): # Pour chaque ligne de la matrice (lettre du polygraph)
		C = 0 # Cipher letter
		for column in range(sizePolyGraph): # Pour chaque coefficient
			coefficient = matrix[row][column] #On récupère le coefficient
			P = ALPHABET.index(plaintextPolygraph[column])+1 # On trouve le chiffre représentant P (indice colonne)
			C += coefficient * P # On ajoute coefficient (indice column) * P (indice column)
		C = C%26 # On revient au modulo 26
		ciphertextPolygraph += ALPHABET[C-1] # On ajoute la lettre trouvée au polygraph
	return ciphertextPolygraph # On renvoie le polygraph


def polygraphicLinearEncipher(plaintext, matrix, sizePolyGraph=2, lettreParDefaut="X"):
	plaintext = deponctuateMessage(plaintext) # Texte à crypter
	indice = 0 # Indice de la lettre
	sizePolyGraph = matrix.shape[0] # Obtient la taille des polygraphs
	ciphertext = "" # Ciphertext
	#* On rajoute des X tant que le message n'a pas une longueur multiple de la taille du polygraph
	while len(plaintext)%sizePolyGraph != 0: # Tant qu'on ne peut pas couper le texte en sections de même longueur
		plaintext+=lettreParDefaut # On ajoute des lettres par défauts
	while indice < len(plaintext):
		# S'il reste encode des lettres pour faire des doublets
		plaintextPolygraph = plaintext[indice:indice+sizePolyGraph]  # On forme le polygraph de taille voulu
		#* On traduit le digraph grâce à la matrix
		ciphertextPolygraph = encipherSinglePolygraph(plaintextPolygraph, matrix, sizePolyGraph)
		indice += sizePolyGraph
		ciphertext += ciphertextPolygraph
	return prettifyCiphertext(ciphertext, 5)

Messages = [" 	Ebgngr zr 13 cynprf!", "YITJP GWJOW FAQTQ XCSMA ETSQU SQAPU SQGKC PQTYJ", "MWALO LIAIW WTGBH JNTAK QZJKA ADAWS SKQKU AYARN CSODN IIAES OQKJY B "]
matriceEncipher = np.array([[3, 4], [11, 23]], dtype=np.integer, ndmin=2)

# matriceDecipher = np.linalg.inv(matriceEncipher).astype(int)
# print(matriceDecipher)

# print(Messages[0])
# print(polygraphicLinearEncipher(Messages[0], matriceEncipher))

# A = np.array([[5,6],[7,3]])
# # B = np.array([[1,2],[3,5]])
# # print(np.matmul(B,A)%26)
# print(np.matmul(A, np.linalg.inv(A)))

# place_in_alphabet("ORG")
# print(resol_modulo(15,19,26))

for i in range(26):
	print(i, ":", affineDecipher(Messages[0], 1, i))