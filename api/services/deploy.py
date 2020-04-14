import os
import sys
import random
import string
import subprocess


DOCKER_COMPOSE_PATH = "/srv/deployment/docker-compose.yml"

class DeployService:

    def __init__(self):
        self.fetchDockerComposeServices()
        self.checkDockerComposeFile()
        self.loginEnabled = False
        
    def fetchDockerComposeServices(self):
        self.services = os.environ['DOCKER_COMPOSE_SERVICES']
        self.services = self.services.strip()
        if not self.services or len(self.services) < 1:
            print("Environment variable DOCKER_COMPOSE_SERVICES not set, aborting.", file=sys.stdout)
            exit()
        print("docker-compose services to be deployed:", self.services)
        
    def checkDockerComposeFile(self):
        if not os.path.isfile(DOCKER_COMPOSE_PATH):
            print("No file found at path "+DOCKER_COMPOSE_PATH+". Make sure docker-compose.yml is mounted there", file=sys.stdout)
            exit()
        print("Found docker-compose.yml at path: "+DOCKER_COMPOSE_PATH)

    def getBaseCommand(self):
        return "docker-compose -f \""+DOCKER_COMPOSE_PATH+"\""
        
    def getPullCommand(self):
        cmd = self.getBaseCommand() + " pull " + self.services
        return cmd
        
    def getDownCommand(self):
        cmd = self.getBaseCommand() + " down"
        return cmd
        
    def getUpCommand(self):
        cmd = self.getBaseCommand() + " up -d "+ self.services
        return cmd
        
    def runCommand(self, cmd, printCmd = True):
        if printCmd:
            print("RUNNING COMMAND:", file=sys.stdout)
            print(cmd, file=sys.stdout)
        proc = subprocess.run([cmd], stdout=sys.stdout, stderr=sys.stderr, shell=True)
        
    def loginToRegistry(self):
        print("logging in to registry", file=sys.stdout)
        cmd = "docker login " + self.secrets['domain'] + " -u " + self.secrets['user'] + " -p " + self.secrets['password']
        self.runCommand(cmd, printCmd = False)
        
    def setSecrets(self, secrets):
        print("enabling login", file=sys.stdout)
        self.loginEnabled = secrets is not None
        self.secrets = secrets
        
    def performDeploy(self):
        print("----- DEPLOYING -----", file=sys.stdout)
        if self.loginEnabled:
            self.loginToRegistry()
            
        self.runCommand(self.getDownCommand())
        self.runCommand(self.getPullCommand())
        self.runCommand(self.getUpCommand())
        sys.stdout.flush()
        sys.stderr.flush()
