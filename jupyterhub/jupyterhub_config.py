## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## LDAP Authenticator
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = 'ldap.ncsa.illinois.edu'
c.LDAPAuthenticator.use_ssl = True
c.LDAPAuthenticator.bind_dn_template = [
    "uid={username},ou=people,dc=ncsa,dc=illinois,dc=edu",
]
c.LDAPAuthenticator.allowed_groups = [
    "cn=prj_cg_isgs,ou=groups,dc=ncsa,dc=illinois,dc=edu",
]

c.Authenticator.admin_users = { 'jefft' }


## Docker spawner
import os

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.volumes = { 
    'jupyterhub-user-{username}': os.path.join(notebook_dir, 'work'),

    '/mnt/nrcs/isgs': {
        'bind': os.path.join(notebook_dir, 'isgs'), 'mode': 'rw',
    },
    '/mnt/nrcs/isgs/lidar': {
        'bind': os.path.join(notebook_dir, 'lidar'), 'mode': 'ro'
    },
    '/mnt/nrcs/isgs/output/pp2g': {
        'bind': os.path.join(notebook_dir, 'dem'), 'mode': 'ro'
    },
    '/mnt/nrcs/jupyterhub/examples': {
        'bind': os.path.join(notebook_dir, 'examples'), 'mode': 'ro'
    },
}

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
