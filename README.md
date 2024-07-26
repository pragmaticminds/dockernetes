# Dockernetes

This brings the simplicity of Kubernetes Monitoring to docker.

## Running the API

Just run the FastAPI

```bash
uvicorn main:app
```

## Connecting to the cluster

Just set the `dockernetes.yaml` file as your kubernetes config file, e.g. with

```bash
export KUBECONFIG=dockernetes.yaml
```

and then

**Have fun**