import json
from json.decoder import JSONDecodeError
import sys
import boto3
import base64

SECRETS_FILE = "/srv/registry_credentials.json"

KEY_REGISTRY_DOMAIN = "domain"
KEY_REGISTRY_USER = "user"
KEY_REGISTRY_PASSWORD =  "password"

KEY_AWS_ACCESSKEY = "aws_access_key_id"
KEY_AWS_SECRET = "aws_secret_access_key"
KEY_AWS_REGION = "region"

class SecretService:

    def __init__(self):
        self.loadSecrets(SECRETS_FILE)
    
    def loadSecrets(self, filename):
        try:
            with open(filename, 'r') as fin:
                txt = fin.read()
                credentials = json.loads(txt)
                
                if KEY_AWS_ACCESSKEY in credentials:
                    self.authenticate_ecr(credentials)
                else:
                    self.authenticate_registry(credentials)
                
        except (IOError, JSONDecodeError) as e:
            print(e)
            print("Did not find a valid secret with Docker registry login")
            
            
    def authenticate_registry(self, credentials):
        self.secrets = credentials
        if self.secrets and KEY_REGISTRY_DOMAIN in self.secrets and KEY_REGISTRY_USER in self.secrets and KEY_REGISTRY_PASSWORD in self.secrets:
            print("Secret for Docker registry login loaded successfully", file=sys.stdout)
        else :
            self.secrets = None
            print("Secret for Docker registry login incomplete", file=sys.stdout)
        
    
    
    def authenticate_ecr(self, credentials):
        # Parse required params 'aws_access_key_id' AND 'aws_secret_access_key'
        aws_access_key_id = credentials[KEY_AWS_ACCESSKEY]
        aws_secret_access_key = credentials[KEY_AWS_SECRET]
        region = credentials[KEY_AWS_REGION]
        # Create a sessions with the credentials
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        # Get authToken from the ECR client
        ecrClient = session.client('ecr', region_name=region)
        token = ecrClient.get_authorization_token()

        # Parse username,password and registry from this token
        user, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        domain = token['authorizationData'][0]['proxyEndpoint']

        if user is not None and password is not None and domain is not None:
            self.secrets = {
                "user": user,
                "password": password,
                "domain": domain
            }
            print("Secret for AWS ECR registry login loaded successfully", file=sys.stdout)
        else :
            self.secrets = None
            print("Secret for AWS ECR registry login incomplete", file=sys.stdout)
        
