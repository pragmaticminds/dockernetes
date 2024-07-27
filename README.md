# Dockernetes

This brings the simplicity of Kubernetes Monitoring to docker.

## Running the API

Just run the FastAPI

```bash
uvicorn main:app --port 6443 --ssl-keyfile dockernetes.key --ssl-certfile dockernetes.crt --host 0.0.0.0
```

## Connecting to the cluster

Just set the `dockernetes.yaml` file as your kubernetes config file, e.g. with

```bash
export KUBECONFIG=dockernetes.yaml
```

and then

**Have fun**

# Explanaition of all the key-stuff

`myCA.*` is the CA for the SSH Certs for the https auth of the cluster.

`dockernetes.*` is all the ssl-related stuff.
The CA (which is also in the yaml), the csr and finally the crt.
See also `sign_certs.sh`.

For JWT we also use RSA with the `dockernetes_jwt.*` files.
