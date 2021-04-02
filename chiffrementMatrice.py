import sys
import random

input = sys.stdin.readline


# plaintext ==> texte non chiffré
# ciphertext ==> texte chiffré
# keyM ==> matrice 2*2 qui est la clef de chiffrement

ALPHABET = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-+?,.;/:'!%<>()[]{} ", 
            "§?0[EFRIZ.{)!VUW AQK>%1N7,2G-6P8Y/;/S:}5XTH<D(3CJ]OB4L+9M"]

def mixAlphabet(typeAlphabet):
    alpha = list(range(len(ALPHABET[typeAlphabet])))
    random.shuffle(alpha)
    print("".join([ALPHABET[typeAlphabet][x] for x in alpha]))

def determinant(matrice):
    det = matrice[0][0] * matrice[1][1] - matrice[1][0] * matrice[0][1] # pour un matrice [[a, b], [c, d]] :
    # le determinant est a*d - b*c
    return det

def inverseMatrix(matrice, typeAlphabet=0):
    """
    Matrice = liste de liste de int
    """
    det = determinant(matrice)
    assert (det == 1) or (det == -1)
    lenAlph = len(ALPHABET[typeAlphabet])

    # assert det != 0, "Erreur, le déterminant doit être non nul!"
    # assert not (len(ALPHABET[typeAlphabet]) % det == 0), "Erreur, le déterminant le doit pas diviser la longueur de l'alphab"

    (a, b), (c, d) = matrice # on suppose ici que la matrice est de format 2x2

    newMatrix = [[lenAlph + (d//det),   lenAlph - (b // det)],
                [lenAlph - (c // det), lenAlph + (a//det)]]

    return newMatrix

def multiplication(keyM, digramme):
    """
    keyM : matrice clé
    Renvoie une liste x' et y'
    """
    (a, b), (c, d) = keyM # on suppose ici que la matrice est de format 2x2
    x, y = digramme
    return [int(a*x+b*y), int(c*x+d*y)]


def dechiffrement(ciphertext, keyM, typeAlphabet=0):
    decipherM = inverseMatrix(keyM, typeAlphabet)
    # print(decipherM)
    return chiffrement(ciphertext, decipherM, typeAlphabet)

def chiffrement(plaintext, keyM, typeAlphabet=0):
    
    alpha = ALPHABET[typeAlphabet]
    caraRemplacement = alpha[-1]
    # caraRemplacement = "_"

    if len(plaintext) % 2 == 1:# Si on a un nombre impair de caractères, il faut en ajouter un cara
        plaintext += alpha[-1] # On ajoute le dernier caractère de l'alphabet
    
    plaintext = plaintext.upper()
    ciphertext = "" 
    
    for i in range(0,len(plaintext), 2): # Pour chaque couple
        digram = [alpha.index(car) if car in alpha else len(alpha)-1 for car in plaintext[i:i+2]] # On extrait le digram
        ciphertext += "".join([alpha[x%len(alpha)] for x in multiplication(keyM, digram)]) # On le chiffre et on l'ajoute au ciphertext

    return ciphertext # on renvoie la réponse


keys = [
    [[5,2],
    [7,3]],

    [[1,2], 
    [3,4]],

    [[3,2], 
    [3,5]],
]

if __name__ == '__main__':
    generatedInput = True
    if generatedInput :
        clef = 0
        typeAlpha = 1
        plaintext = "BONJOUR, BRAVO D'AVOIR DECODE L'IMPOSSIBLE"
    else :
        clef = int(input())
        typeAlpha = int(input())
        plaintext = input().strip()
    C = chiffrement(plaintext, keys[clef], typeAlpha)
    print(f"Texte après encryptage : {C}")
    # print(plaintext)
    print(f"Texte après décryptage par matrice inverse : {dechiffrement(C, keys[clef], typeAlpha)}")

    ciphertext = "G64-QYL+/H}Z-K-AO§W;{Q[RJ-[U"
    typeAlpha = 1 
    clef = 0
    print(dechiffrement(ciphertext, keys[clef], typeAlphabet=1))