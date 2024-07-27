#!/usr/bin/env python
"""
This file can be used to generate JWT Tokens for custom user based kubernetes config files
"""
import datetime
import sys
import uuid

import jwt

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python generate_token.py <username>"

    username = sys.argv[1]

    with open("dockernetes_jwt.pem", "rb") as f:
        private_key = f.read()

    encoded = jwt.encode({
        "iss": "kubernetes/serviceaccount",
        "kubernetes.io/serviceaccount/namespace": "kube-system",
        "kubernetes.io/serviceaccount/secret.name": "cluster-admin-token-r29mg",
        "kubernetes.io/serviceaccount/service-account.name": username,
        "kubernetes.io/serviceaccount/service-account.uid": uuid.uuid4().__str__(),
        "sub": f"system:serviceaccount:kube-system:{username}",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)}, key=private_key, algorithm="RS256")

    print("Your Token is:")
    print(encoded)
