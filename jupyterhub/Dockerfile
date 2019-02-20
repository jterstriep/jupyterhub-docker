FROM jupyterhub/jupyterhub:0.9.3

RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/0.9.3/examples/cull-idle/cull_idle_servers.py

RUN pip install \
    jupyterhub-ldapauthenticator==1.2.2 \
    dockerspawner==0.10.0 \
    oauthenticator==0.8.0

COPY jupyterhub_config.py .
