import docker
import configparser

CONFIG_PATH = 'backend/backend/config.ini'

def get_url(container_name: str, container) -> str:
    inner_ip: str = container.attrs['NetworkSettings']['Networks']['mse1h2024-assistant_main']['IPAddress']
    port_key: str = list(container.attrs['NetworkSettings']['Ports'].keys())[0]
    inner_port: str = container.attrs['NetworkSettings']['Ports'][port_key][0]['HostPort']
    model_url: str = 'http://{0}:{1}'.format(inner_ip, inner_port)
    return model_url


client = docker.DockerClient()
config = configparser.ConfigParser()
ollama_container = client.containers.get('ollama')
model_url = get_url('ollama', ollama_container)

whisper_container = client.containers.get('whisper')
whisper_url = get_url('whisper', whisper_container)

config.read(CONFIG_PATH)
config['model']['url'] = model_url
config['whisper']['url'] = whisper_url
print(whisper_url)

with open(CONFIG_PATH, 'w') as configfile:
    config.write(configfile)