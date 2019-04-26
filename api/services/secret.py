import json
from json.decoder import JSONDecodeError
import sys

SECRETS_FILE = "/srv/registry_credentials.json"


class SecretService:

    def __init__(self):
        self.loadSecrets(SECRETS_FILE)
    
    def loadSecrets(self, filename):
        self.loginEnabled = False
        try:
            with open(filename, 'r') as fin:
                txt = fin.read()
                self.secrets = json.loads(txt)
                if self.secrets and self.secrets['domain'] and self.secrets['user'] and self.secrets['password']:
                    self.loginEnabled = True
                    print("Secret with Docker registry login loaded successfully", file=sys.stdout)
                else :
                    print("Secret with Docker registry login incomplete", file=sys.stdout)
        except (IOError, JSONDecodeError) as e:
            print("Did not find a valid secret with Docker registry login")
