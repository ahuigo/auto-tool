#!/usr/bin/env python3
import argparse
import os,sys
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("suffix", help="helm suffix like: dev|staging|_ack_dev|...")
args = parser.parse_args()

def initYaml():
    from ruamel.yaml.representer import RoundTripRepresenter
    from ruamel.yaml import YAML
    def repr_str(dumper: RoundTripRepresenter, data: str):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml = YAML()
    yaml.representer.add_representer(str, repr_str)
    return yaml

yaml = initYaml()
def yamlDump(data):
    from io import StringIO
    f = StringIO()
    yaml.dump(data, f)
    #yaml.dump(data, sys.stdout)
    return f.getvalue()


class ParseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def yesno(tips="overvide conf?(y/n)(default:y)"):
    a = input(tips)
    if a not in ("y",""):
        quit("quit")

def getHelmPath(suffix):
    import glob
    home = os.getenv('HOME')
    appname = Path('.').absolute().name
    helmDir = home + f'/hdmap/hdmap-helm-charts/{appname}'
    for filepath in glob.glob(f'{helmDir}/*{suffix}.yaml'):
        return filepath
    raise ParseException('Could not find helm path for:'+appname, helmDir)

def getHelmConf(suffix):
    helmPath = getHelmPath(suffix)
    conf = yaml.load(open(helmPath,'r'))
    if 'configMap' in conf:
        configMap = conf['configMap']['file']['data']
        d = list(configMap.values())[0]
        d = yaml.load(d)
        return d
    else:
        quit(f'Could not find configMap data')

localConf = yaml.load(open(Path.home()/'.mo.yaml')).get('helm', {})
def handleEndpoint(url,suffix):
    print(url,localConf)
    endpoints = localConf.get(url,None)
    if endpoints:
        for env,endpoint in endpoints.items():
            if suffix.endswith(env):
                return endpoint
        quit(f'coulnd find value for:{url}')
    return url
    

from collections import OrderedDict
from ruamel.yaml.comments import CommentedSeq
def handleK8sYaml(conf, suffix):
    print('conf:', type(conf),conf)
    for k,v in conf.items():
        if isinstance(v, OrderedDict):
            handleK8sYaml(v, suffix)
        elif isinstance(v, CommentedSeq):
            conf[k]=[handleEndpoint(vv, suffix) for vv in v]
            # print('v',v)
            # for item in v:
            #     handleK8sYaml(item, suffix)
        elif isinstance(v, str) and ':' in v:
            conf[k]=handleEndpoint(v, suffix)
            # print(k,type(v), v)

def importHelmConf(suffix):
    data = getHelmConf(suffix)
    handleK8sYaml(data, suffix)
    output = yamlDump(data)
    print(output)
    p = Path('./config/conf.yaml')
    if p.exists():
        yesno(f"overvide:./conf.yaml?")
        p.unlink()
    open(p,'w').write(output)
    print('write success')

if __name__ == '__main__':
    suffix = args.suffix
    try:
        importHelmConf(suffix)
    except ParseException as e:
        print(e.args)
