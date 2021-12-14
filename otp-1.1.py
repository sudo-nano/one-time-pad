#!/usr/bin/env python3

import string
import random
import sys
import time

abc = string.ascii_lowercase
ABC123 = string.ascii_uppercase + "1234567890" #defines ABC123, the character set for encryption and decryption consisting of all uppercase letters and numbers
one_time_pad = list(abc)
keyArray = []

help = """Synopsis: otp.py -e|-d

-e encrypt
-d decrypt 
-g <number> | generate key of the specified length"""


def encrypt(msg, key):
    ciphertext = ''
    for idx, char in enumerate(msg): #idx is short for index
        charIdx = ABC123.index(char) #returns the position of the given character in the string containing the character set
        keyIdx = ABC123.index(key[idx])

        cipherint = (keyIdx + charIdx)

        if cipherint > len(ABC123):                  #If cipherint is larger than the length of the character list, 
            cipherint = cipherint - len(ABC123)      #subtract char list length from it to make it wrap.
            print("Debug: Wrapping cipherint index")

        ciphertext += ABC123[cipherint]

    return ciphertext


def decrypt(ciphertext, key):
    if ciphertext == '' or key == '':
        return ''

    charIdx = ABC123.index(ciphertext[0])
    keyIdx = one_time_pad.index(key[0])

    cipher = (charIdx - keyIdx) % len(one_time_pad)
    char = ABC123[cipher]

    return char + decrypt(ciphertext[1:], key[1:])

def genkey(keylength):

    try:
        if int(keylength) < 0:
            return "Invalid key length. Use a positive integer."

        else:
            lengthInt = int(keylength)
            spaceCharCounter = 0
            spaceCounter = 0
            while lengthInt > 0:

                if spaceCharCounter == 5:
                    keyArray.append(" ")
                    spaceCharCounter = 0
                    spaceCounter += 1 #spaceCounter is iterated to add line breaks after every four spaces

                if spaceCounter == 4:
                    keyArray.append("\n")
                    spaceCounter = 0

                keyArray.append(random.choice(ABC123))
                lengthInt -= 1
                spaceCharCounter += 1 #spaceCharCounter is iterated with each letter so that a space can be added every five letters

            if lengthInt == 0:
                emptyString = ""
                return(emptyString.join(keyArray))

    except:
        return "Invalid key length. Use a positive integer."
        
'''
To Do: 
- Fix decryption function to work with all alphanumeric characters

- Add function that saves location of capitalization, punctuation, and white space
- Add function that restores saved capitalization, punctuation, and white space
- Add formatting preservation to encryption function
- Add formatting preservation to decryption function

- Add ability to save keys to file (make it a prompt after key generation to avoid dealing with multiple argument shenanigans)
- Add ability to load keys from file as second and third arguments (-k <keyfile>)



Optional: 
- Add ability to load and save ciphertext from file
- Add ability to load and save plaintext from file

Done: 
- Fix encryption function to work with all alphanumeric characters
'''



if __name__ == '__main__':
    availableOpt = ["-d", "-e", "-g"]
    if len(sys.argv) == 1 or sys.argv[1] not in availableOpt:
        print(help)
        exit(0)

    if sys.argv[1] != availableOpt[2]:
        keyRaw = input("Key: ")
        msgRaw = input("Message: ")

        keyUpper = keyRaw.upper() #Forces key to be uppercase
        key = keyUpper.replace(" ", "") #Removes whitespace from key 

        msgUpper = msgRaw.upper() #Forces message to be uppercase
        msg = msgUpper.replace(" ", "") #Removes whitespace to prevent exceptions

    if sys.argv[1] == availableOpt[1]:
        print(encrypt(msg, key))
    elif sys.argv[1] == availableOpt[0]:
        print(decrypt(msg, key))
    elif sys.argv[1] == availableOpt[2]:
        print(genkey(sys.argv[2]))