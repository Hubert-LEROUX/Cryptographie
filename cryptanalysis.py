import csv
from collections import Counter
import pandas as pd
from commonTools import desaccentueMessage, substitution_dict_maker

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
STRING_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def write_csv(list_ciphertext):
	"""
	Enregistre un fichier csv avec le nombre d'occurences de chaque caractère
	:param list_ciphertext: list des ciphertext à analyser
	:return: ø
	"""
	liste_occurences_dict = []
	for ciphertext in list_ciphertext:
		liste_occurences_dict.append(Counter(ciphertext))
	with open("analyse.csv", 'w', newline='') as fich:
		analyse_csv = csv.writer(fich, delimiter=';')
		# for key in occurences_dict.keys():
		# 	analyse_csv.writerow([key, str(occurences_dict[key])])
		for l in ALPHABET:
			row = [str(l)] + [str(occurences_dict[str(l)]) for occurences_dict in liste_occurences_dict]
			analyse_csv.writerow(row)

def analyse_digraphs(cip: str, long: int = 2, n_common: int = 10) -> None:
	cip = list(cip.replace(' ', '').upper())
	digraphs = []
	for i in range(len(cip)-long):
		digraphs.append(''.join(cip[i:i+long]))
	digraphs_count = Counter(digraphs).most_common(n_common)
	with open("analyse_digraphs.csv", 'w', newline='') as fich:
		analyse_csv = csv.writer(fich, delimiter=';')
		analyse_csv.writerow(["Digraphs", "N_Occurences"])
		for dig, occur in digraphs_count:
			row = [dig, occur]
			analyse_csv.writerow(row)

def tableau(cip):
	cip = list(cip.replace(' ', '').upper())
	tableau = [[] for i in range(26)]
	for i in range(len(cip)):
		# print(alphabet.index(cip[i]))
		# print(tableau[alphabet.index(cip[i])])
		# print(tableau)
		if i <= 0:
			tableau[ALPHABET.index(cip[i])].append('*'+cip[i+1])
		elif i == len(cip)-1:
			tableau[ALPHABET.index(cip[i])].append(cip[i-1] + '*')
		else:
			tableau[ALPHABET.index(cip[i])].append(cip[i-1] + cip[i+1])
	# Réalise le tableau
	df = pd.DataFrame(columns=ALPHABET)
	maximum = max([len(l) for l in tableau])
	for ind_row in range(maximum):
		row = []
		for i in range(26): # Pour toutes les lettres de l'alphabet
			if ind_row < len(tableau[i]):   # S'il reste des digraphs pour cette lettre
				row.append(tableau[i][ind_row]) # On ajoute ce digraph à la ligne
			else:
				row.append("")   # Sinon on ajoute une chaîne de caractère vide
		# print(row)
		df.loc[ind_row] = row # On ajoute la ligne au df
	df.to_csv('Tableau.csv', sep=';', index=False)
	return df

def search_word(wordToGuess, language="FRENCH"):
	"""
	Cherche toute les possibilités pour un mot où les étoiles "*" indiquent les lettres manquantes
	Les languages possibles sont "FRENCH", "ENGLISH"
	"""
	LIST_WORDS_FILE = "WordList/liste_francais.txt" # Fichier txt contenant une liste de mots (en français si on ne saisi pas correctement le language)
	if language == "FRENCH": LIST_WORDS_FILE = "WordList/liste_francais.txt" # Liste de mots pour le français
	elif language == "ENGLISHH": LIST_WORDS_FILE = "WordList/3000_most_common_words.txt" # LIste de mots pour l'anglais
	print("Possibilities for "+wordToGuess+' :') # Affiche une introduction pour les résultats
	wordToGuess = list(wordToGuess.upper()) # Transforme le mot en liste
	matches = [] # Liste des mots ayant "matchés"
	with open(LIST_WORDS_FILE, 'r', newline='\n') as fich: # Ouverture du fichier contenant la liste de mots
		for word in fich: # Pour chaque mot dans la liste
			word = list(desaccentueMessage(word.replace('\r', '').replace('\n', ''))) # CLean le mot
			if len(word) == len(wordToGuess): # Si le mot correspondant a la même longueur que le mot partiel à deviener...
				same = True # On part de l'hypothèse qu'ils sont identiques
				for i in range(len(wordToGuess)): # On effectue alors une boucle de lalongueur du mot
					if wordToGuess[i] != '*' and wordToGuess[i].upper() != word[i]: # Si, lorsque le mot partiel, on connaît une lettre, mais que cette lettre ne correspond pas au mot de la liste...
						same = False # L'Hypothèse devient alors fausse
						break # Pas la peine d'aller plus loin
				if same: # Si l'hypothèse n'a pas pu être rejété, le mot est possiblement bon
					print(''.join(word)) # Alors on l'affiche
					matches.append(''.join(word))
	return matches # On retourne les matches


def remplace1(ciphertext, plainAlphabet):
	"""
	Remplace les lettres dont on connaît la correspondance
	:param ciphertext: Texte crypté
	:param plainAlphabet: Alphabet plaintext
	:return: plaintext
	"""
	substitution = substitution_dict_maker(plainAlphabet)
	plaintext = ""
	for letter in ciphertext:
		if letter in ALPHABET:
			plaintext += substitution[letter]
		else:
			plaintext += letter
	return plaintext


def remplace2(ciphertext, cipherAlphabet):
	"""
	Remplace les lettres dont on connaît la correspondance
	:param ciphertext: Texte chiffré
	:param cipherAlphabet: Alphabet ciphertext
	:return: Plaintext
	"""
	cipherAlphabet = list(cipherAlphabet)
	plaintext = ""
	for letter in ciphertext:
		if letter in cipherAlphabet:
			plaintext += ALPHABET[cipherAlphabet.index(letter)]
		elif letter in ALPHABET:
			plaintext += '#'
		else:
			plaintext += letter
	return plaintext








