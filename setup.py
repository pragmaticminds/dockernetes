"""
This file generates all the necessary certs and yamls for the dockernetes project
"""
import base64
import datetime
import random
import re
import sys
import uuid

import jwt
from OpenSSL import crypto

if __name__ == "__main__":
    # We get the hostname as the first parameter
    assert len(sys.argv) >= 2, "Usage: python setup.py <hostname> (<username>)"
    hostname = sys.argv[1]
    if len(sys.argv) == 3:
        username = sys.argv[2]
    else:
        username = None

    # Now we generate our root CA
    # Check if a root CA exists
    try:
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open("ca.key", "rt").read())
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open("ca.crt", "rt").read().encode())
        print("Using CA loaded from filesystem")
    except:
        print("Generating Root CA")

        ###########
        # CA Cert #
        ###########

        ca_key = crypto.PKey()
        ca_key.generate_key(crypto.TYPE_RSA, 2048)

        ca_cert = crypto.X509()
        ca_cert.set_version(2)
        ca_cert.set_serial_number(random.randint(50000000, 100000000))

        ca_subj = ca_cert.get_subject()
        ca_subj.commonName = "My CA"

        ca_cert.add_extensions([
            crypto.X509Extension("subjectKeyIdentifier".encode(), False, "hash".encode(), subject=ca_cert),
        ])

        ca_cert.add_extensions([
            crypto.X509Extension("authorityKeyIdentifier".encode(), False, "keyid:always".encode(), issuer=ca_cert),
        ])

        ca_cert.add_extensions([
            crypto.X509Extension("basicConstraints".encode(), False, "CA:TRUE".encode()),
            crypto.X509Extension("keyUsage".encode(), False, "keyCertSign, cRLSign".encode()),
        ])

        ca_cert.set_issuer(ca_subj)
        ca_cert.set_pubkey(ca_key)
        ca_cert.sign(ca_key, 'sha256')

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)

        # Save certificate
        with open("ca.crt", "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert).decode())

        # Save private key
        with open("ca.key", "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key).decode())

    ###############
    # Client Cert #
    ###############

    # Check if a client cert exists
    try:
        client_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open("client.key", "rt").read())
        client_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open("client.crt", "rt").read().encode())
        print("Using Client loaded from filesystem")
    except:
        print("Generating Client Cert")

        client_key = crypto.PKey()
        client_key.generate_key(crypto.TYPE_RSA, 2048)

        client_cert = crypto.X509Req()
        client_cert.set_version(0)
        # client_cert.set_serial_number(random.randint(50000000, 100000000))

        # client_subj = client_cert.get_subject()
        # client_subj.commonName = "Client"

        # client_cert.add_extensions([
        #     crypto.X509Extension("basicConstraints".encode(), False, "CA:FALSE".encode()),
        #     crypto.X509Extension("subjectKeyIdentifier".encode(), False, "hash".encode(), subject=ca_cert),
        # ])
        #
        # client_cert.add_extensions([
        #     crypto.X509Extension("authorityKeyIdentifier".encode(), False, "keyid:always".encode(), issuer=ca_cert),
        #     crypto.X509Extension("extendedKeyUsage".encode(), False, "clientAuth".encode()),
        #     crypto.X509Extension("keyUsage".encode(), False, "digitalSignature".encode()),
        # ])

        if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', hostname):
            # its an IP
            print("Hostnmae is an IP, using it...")
            alt_name = f"IP.1:{hostname}"
        else:
            print("Hostname seems to be DNS, using it...")
            alt_name = f"DNS.1:{hostname}"

        client_cert.add_extensions([
            crypto.X509Extension(b"subjectAltName", False, alt_name.encode()),
        ])

        # client_cert.set_issuer(ca_subj)
        client_cert.set_pubkey(client_key)

        client_cert.sign(ca_key, 'sha256')

        # Now we have the csr
        # with open("client.csr", "wt") as f:
        #     f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, client_cert).decode())

        cert = crypto.X509()
        cert.set_version(2)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(5 * 365 * 24 * 60 * 60)
        cert.set_issuer(ca_cert.get_subject())
        cert.set_subject(client_cert.get_subject())
        cert.set_pubkey(client_cert.get_pubkey())
        cert.add_extensions(client_cert.get_extensions())
        cert.sign(ca_key, 'sha256')

        # client_cert.gmtime_adj_notBefore(0)
        # client_cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)

        # Save certificate
        with open("client.crt", "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())

        # Save private key
        with open("client.key", "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key).decode())

    print("Public and Private Key for JWT Token")
    # Try to laod it from file
    try:
        jwt_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open("jwt.pem", "rt").read())
        print("Using JWT loaded from filesystem")
    except:
        # Generate the public / private key pair for jwt with RSA256
        jwt_key = crypto.PKey()
        jwt_key.generate_key(crypto.TYPE_RSA, 2048)
        # Save private and public key
        with open("jwt.pem", "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, jwt_key).decode())
        with open("jwt.crt", "wt") as f:
            f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, jwt_key).decode())

    if username is not None:
        print(f"Generating JWT Token and kubeconfig file for user {username}")
        # With this we can now also generate a jwt token
        token = jwt.encode({
            "iss": "kubernetes/serviceaccount",
            "kubernetes.io/serviceaccount/namespace": "kube-system",
            "kubernetes.io/serviceaccount/secret.name": "cluster-admin-token-r29mg",
            "kubernetes.io/serviceaccount/service-account.name": username,
            "kubernetes.io/serviceaccount/service-account.uid": uuid.uuid4().__str__(),
            "sub": f"system:serviceaccount:kube-system:{username}",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)},
            key=crypto.dump_privatekey(crypto.FILETYPE_PEM, jwt_key).decode(), algorithm="RS256")

        print("Generating Kubeconfig")


        def generate_kubeconfig(ca, hostname, token):
            return f"""apiVersion: v1
kind: Config
preferences: {{}}
current-context: dockernetes@Dockernetes
clusters:
- cluster:
    certificate-authority-data: {ca}
    server: https://{hostname}:6443
  name: !!str Dockernetes
contexts:
- context:
    cluster: !!str Dockernetes
    user: dockernetes
  name: dockernetes@Dockernetes
users:
- name: dockernetes
  user:
    token: {token}
"""


        with open("ca.crt", "rt") as f:
            ca = base64.b64encode(f.read().encode()).decode()

        with open("kubeconfig.yaml", "wt") as f:
            f.write(generate_kubeconfig(ca, hostname, token))

        print("Done")
