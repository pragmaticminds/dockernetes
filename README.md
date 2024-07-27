# Dockernetes

![Dockernetes](logos/_96eacb8b-5bd5-4eab-9153-764d43d174fc.jpg)

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

# Issue cusstom kubernetes configs

Just copy the `dockernetes.yaml` file and simply replace the "token" in the last line with the output of a call to `generate_token.py <username>` (this is not really relevant but makes the logging a bit nicer). 

# Generate new Certs / CSRs for new deployments

First, generate a private key
```bash
openssl genrsa -out dockernetes.key 2048 
```
then a CSR
```bash
 openssl req -new -key dockernetes.key -out dockernetes.csr 
```
then update the ext file
`dockernetes.ext` witht he right IP (or DNS).
Beware that you need to write either
```
IP.1 = 192.168.167.180
or
DNS.1 = localhost
```

Finally, sign the cert
```bash
openssl x509 -req -in dockernetes.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out dockernetes.crt -days 500 -sha256 -extfile dockernetes.ext
```

# compress folder
    
    ```bash
    tar -czvf dockernetes.tar.gz dockernetes
    ```

# decompress folder

    ```bash
    tar -xzvf dockernetes.tar.gz
    ```