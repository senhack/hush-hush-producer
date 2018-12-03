import configparser
import requests
import hush.audio


class ConfigError(Exception):
    pass


class _Config:
    def __init__(self, config_file):
        cfg = configparser.RawConfigParser()
        cfg.read(config_file)

        if len(cfg.sections()) == 0:
            raise ConfigError("failed to open config file: {0}".format(config_file))

        if not cfg.has_section('hush'):
            raise ConfigError("config section 'hush' missing")

        self.url = cfg.get('hush', 'url')
        self.device = cfg.get('hush', 'device')
        self.key = cfg.get('hush', 'key')


class LambdaError(Exception):
    pass


class _AWSLambda:
    def __init__(self):
        if hconfig == None:
            raise LambdaError("Configuration missing")

        self.headers = {
            'Content-type': 'application/json',
            'x-api-key': hconfig.key
        }

    @property
    def status(self):
        r = requests.get(
                "{0}/{1}".format(hconfig.url, hconfig.device),
                headers=self.headers)
        r.raise_for_status()

        return r.json()

    def push_stats(self, data):
        r = requests.post(
                "{0}/{1}".format(hconfig.url, hconfig.device),
                data=json.dumps(data),
                headers=self.headers)
        r.raise_for_status()


def start(config_file):
    global hconfig
    global awslambda

    hconfig = _Config(config_file)
    awslambda = _AWSLambda()

    hush.audio.Mic(hconfig, awslambda)


def stop():
    hush.audio.Mic.clean()
