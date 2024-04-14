import docker
import configparser

CONFIG_PATH = 'backend/backend/config.ini'

client = docker.DockerClient()
config = configparser.ConfigParser()
container = client.containers.get('ollama')
inner_ip: str = container.attrs['NetworkSettings']['Networks']['mse1h2024-assistant_main']['IPAddress']
port_key: str = list(container.attrs['NetworkSettings']['Ports'].keys())[0]
inner_port: str = container.attrs['NetworkSettings']['Ports'][port_key][0]['HostPort']
model_url: str = 'http://{0}:{1}'.format(inner_ip, inner_port)

config.read(CONFIG_PATH)
config['model']['url'] = model_url

with open(CONFIG_PATH, 'w') as configfile:
    config.write(configfile)