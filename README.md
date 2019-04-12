# Docker-compose deployer over HTTP
This tool can be installed on a server that is controlled by [docker-compose](https://docs.docker.com/compose/) for tis deployments. After doing so, a webhook becomes available on `POST serverdomain:12045/deploy` to perform a deploy. This enables deployments via CI without providing SSH access.

## Setup
### Setup using Git clone
 1. Clone the current repository on the deployment server.
 2. Overwrite the `deployment/docker-compose.yml` file with the contents of the docker-compose setup you want to deploy.
 3. Adjust the `docker-compose.yml` in the root folder of the project so that the `DOCKER_COMPOSE_SERVICES` environment variable is set to a space-separated list of services. These services should match with those in the `deployment/docker-compose.yml` file that you added in step 2.
 4. Launch with the following command in the root path of the project: `docker-compose up -d deployer`
5. Check the logs via: `docker-compose logs -f deployer`

The token is available in the logs. Perform a HTTP POST request to  `serverdomain:12045/deploy` with the `Authorization` header set to `Bearer <TOKEN>` to deploy an update

### Setup using prebuilt Docker image
This is still WIP.

## Security
Note that this setup is not entirely secure by default:
* The server is prune to (D)DOS attacks 
* The token is sent plain text over HTTP
* The response headers are not secure

A number of those can be fixed by extending the setup with an nginx proxy which takes the requests, applies security measurements and then proxies the request to the deployer service. This can be done in the `docker-compose` on the root level.
