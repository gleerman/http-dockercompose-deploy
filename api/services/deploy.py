import os
import sys
import random
import string
import subprocess
import docker


DOCKER_COMPOSE_PATH = "/srv/deployment/docker-compose.yml"

class DeployService:

    def __init__(self):
        self.docker_client = docker.from_env()
        self.fetchDockerComposeServices()
        self.checkDockerComposeFile()
        
    def loginToRegistry(self, creds):
        self.docker_client.login(registry = creds['domain'], username = creds['user'], password = creds['password'])
        
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
        
    def getDownCommand(self):
        cmd = self.getBaseCommand() + " down"
        return cmd
        
    def getUpCommand(self):
        cmd = self.getBaseCommand() + " up -d "+ self.services
        return cmd
        
    def runCommand(self, cmd):
        print("RUNNING COMMAND:", file=sys.stdout)
        print(cmd, file=sys.stdout)
        proc = subprocess.run([cmd], stdout=sys.stdout, stderr=sys.stderr, shell=True)
        
    def performDeploy(self):
        print("----- DEPLOYING -----", file=sys.stdout)
        self.runCommand(self.getDownCommand())
        self.runCommand(self.getUpCommand())
        sys.stdout.flush()
        sys.stderr.flush()
