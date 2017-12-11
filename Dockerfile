FROM centos:7
RUN yum install -y epel-release && \
    yum-config-manager --enable cr && \
    yum -y install which gcc gcc-c++ kernel-devel vim less mod_ssl \
	make mariadb mariadb-devel python-devel httpd httpd-devel  && \
    yum clean all

# Create a self-signed cert
run mkdir -p /srv/certs
WORKDIR /srv/certs

RUN openssl rand -base64 48 > passphrase.txt
RUN openssl genrsa -des3 -passout file:passphrase.txt -out server.key 1024 

RUN openssl req -new -key server.key -passin file:passphrase.txt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"   -out server.csr
RUN cp server.key server.key.org
RUN openssl rsa -in server.key.org -passin file:passphrase.txt -out server.key
RUN openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

RUN openssl genrsa -des3 -passout file:passphrase.txt -out ca.key 4096
RUN openssl req -new -x509 -days 365 -key ca.key -passin file:passphrase.txt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost" -out ca.crt
RUN openssl genrsa -des3 -out client.key -passout file:passphrase.txt 1024
RUN openssl req -new -key client.key -passin file:passphrase.txt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost" -out client.csr
RUN openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 01 -passin file:passphrase.txt -out client.crt

run chown -R apache /srv/certs

# install Python dependencies
ADD  https://bootstrap.pypa.io/get-pip.py /src/get-pip.py
run python /src/get-pip.py
run pip install mod_wsgi
copy requirements /src/requirements
run pip install -r /src/requirements/local.txt

RUN mkdir -p /srv/mod_wsgi
RUN PYTHONPATH=/src/cfgov-refresh/cfgov && \
    mod_wsgi-express setup-server \
	--https-port 8443 \
	--startup-log \
       	--log-to-terminal \
	--server-name localhost \
	--allow-localhost \
        --ssl-certificate-file /srv/certs/server.crt \
        --ssl-certificate-key-file /srv/certs/server.key \
        --server-root /srv/mod_wsgi \
	--user apache \
	/src/cfgov-refresh/cfgov/cfgov/wsgi.py
RUN sed -i 's/Allow from localhost/Allow from all/g' /srv/mod_wsgi/httpd.conf
# setup entrypoint
copy docker-entrypoint.sh /bin/entrypoint.sh
run chmod +x /bin/entrypoint.sh
