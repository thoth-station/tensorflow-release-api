# Tensorflow Release API
A Service for releasing tensorflow builds deployment.

## Features
- API endpoint for Thoth to make a request for deployment of tensorflow build and jobs when pypi has new version of tensorflow.
- A User can make a request for specific tensorflow build and job based upon specific python version and os version. 

## API Reference
- Enpoint
	- `<url>/tensorflow/release/{tf_version}` 
		- Endpoint for thoth to submit a request for deployment of tensorflow build and jobs when pypi has new version of tensorflow.
	- `<url>/tensorflow/custom-release`
		- Endpoint for User can make a request for specific tensorflow build and job based upon specific python version and os version.

## How to use?
- Deployment  of the service:
	- Provision the Service:
	`ansible
	 $ ansible-playbook --extra-var="OCP_URL=<openshift url> OCP_TOKEN=<openshift token> OCP_NAMESPACE=<openshift namespace> SESHETA_GITHUB_ACCESS_TOKEN=<github_token> OCP_SECRET=<name of the secret>" playbooks/provision.yaml  
	`

	- Deprovision the Service:
	`ansible
	 $ ansible-playbook --extra-var="OCP_URL=<openshift url> OCP_TOKEN=<openshift token> OCP_NAMESPACE=<openshift namespace>" playbooks/deprovision.yaml  
	`

- After the Deployment, a Service will start with the swagger UI at a route.

## License
[GNU General Public License v3.0](https://github.com/thoth-station/tensorflow-release-api/blob/master/LICENSE) ©
