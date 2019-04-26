import os
import sys
import random
import string


TOKEN_PATH = "/srv/token/token.txt"
TOKEN_LENGTH = 32

class TokenService:

    def __init__(self):
        token = self.initializeToken()
        print("Token: ", self.token, file=sys.stdout)
        
        
    def initializeToken(self):
        # check if a token already is set
        self.token = self.readToken()
        
        # if not: generate a new token
        if not self.token:
            tokenWritten = self.generateToken()
            if tokenWritten:
                self.token = self.readToken()
        
        # if both of the above failed, something is off
        if not self.token and not tokenWritten:
            print("Error writing token", file=sys.stdout)
            exit()
        
        
    def generateToken(self):
        newToken = ''.join(random.choices(string.hexdigits, k=TOKEN_LENGTH))

        try:
            file = open(TOKEN_PATH, "w")
            file.write(newToken)
            file.close()
        except (IOError, OSError) as e:
            print("unable to write token", file=sys.stdout)
            print(e, file=sys.stdout)
            return False
        
        return newToken
        

    def readToken(self):
        try:
            file = open(TOKEN_PATH, "r") 
            token = file.read() 
            file.close()
        except (IOError, OSError) as e:
            print("unable to read token", file=sys.stdout)
            print(e, file=sys.stdout)
            return False
        
        return token
        

    def isValidHeader(self, header=None):
        if not header:
            return False
        
        headerToken = None
        try:
            headerToken = header.split(" ")[1]
        except IndexError:
            return False
        
        return headerToken == self.token
