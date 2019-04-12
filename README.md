# Docker-compose deployer over HTTP
This tool can be installed on a server that is controlled by [docker-compose](https://docs.docker.com/compose/) for tis deployments. After doing so, a webhook becomes available on `POST serverdomain:12045/deploy` to perform a deploy. This enables deployments via CI without providing SSH access.

## Setup
 1. Navigate to a desired folder for your deployment setup.
 2. Add a `docker-compose.yml` file and copy the contents from [this repo's file](https://github.com/gleerman/http-dockercompose-deploy/blob/master/docker-compose.yml) into it.
 3. Create a file `deployment/docker-compose.yml` with the contents of the docker-compose setup you want to deploy.
 4. Adjust the `docker-compose.yml` from step 2 so that the `DOCKER_COMPOSE_SERVICES` environment variable is set to a space-separated list of services. These services should match with those in the `deployment/docker-compose.yml` file that you added in step 3.
 5. Launch with the following command in the root path of the project: `docker-compose up -d deployer`
 6. Check the logs via: `docker-compose logs -f deployer`

The token is available in the logs. Perform a HTTP POST request to  `serverdomain:12045/deploy` with the `Authorization` header set to `Bearer <TOKEN>` to deploy an update

## Security
Note that this setup is not entirely secure by default:
* The server is prune to (D)DOS attacks 
* The token is sent plain text over HTTP
* The response headers are not secure

A number of those can be fixed by extending the setup with an nginx proxy which takes the requests, applies security measurements and then proxies the request to the deployer service. This can be done in the `docker-compose` on the root level.
