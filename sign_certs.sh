openssl x509 -req -in dockernetes.csr -CA myCA.pem -CAkey myCA.key \
-CAcreateserial -out dockernetes.crt -days 825 -sha256 -extfile dockernetes.ext