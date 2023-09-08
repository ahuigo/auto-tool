#!/usr/bin/env python3
import argparse
import os,sys
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument('-n','--name', default="", help="helm chart name")
parser.add_argument("envDir", help="helm envDir like: dev|staging|_ack_dev|...")
gargs = parser.parse_args()

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

localConf = yaml.load(open(Path.home()/'.mo.yaml')).get('helm', {})

class ParseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def yesno(tips="overvide conf?(y/n)(default:y)"):
    a = input(tips)
    if a not in ("y",""):
        quit("quit")

def checkHelmGitBranch(path:str):
    from subprocess import getoutput
    if not Path(path).exists():
        quit(f'{path} does not exist')

    oripath=Path.cwd()
    os.chdir(path)
    branch_name = getoutput('git branch --show-current')
    #if branch_name != "cicd-template":
    if branch_name != "cicd":
        quit(f"{path} is not at branch `cicd`, but `{branch_name}`")
    os.chdir(oripath)

def getHelmPath(envDir):
    import glob
    home = os.getenv('HOME') or ''
    helmDir = localConf.get('chart_path', '')
    if not helmDir:
        #helmDir = home + f'/hdmap/hdmap-helm-charts'
        helmDir = home + f'/hdmap/cicd'
    if helmDir.startswith('~/'):
        helmDir = home + helmDir[1:]
    checkHelmGitBranch(helmDir)

    if gargs.name == "":
        appname = Path('.').absolute().name
    else:
        appname = gargs.name

    helmDir += f'/{appname}'
    helmFile = f'{helmDir}/{envDir}/conf.yaml'
    for filepath in glob.glob(helmFile):
        return filepath
    raise ParseException('Could not find helm path for:'+appname, helmFile)

def getHelmConfOld(envDir):
    helmPath = getHelmPath(envDir)
    conf = yaml.load(open(helmPath,'r'))
    if 'configMap' in conf:
        configMap = conf['configMap']['file']['data']
        d = list(configMap.values())[0]
        d = yaml.load(d)
        return d
    else:
        quit(f'Could not find configMap data')

def getHelmConf(envDir):
    helmPath = getHelmPath(envDir)
    print(helmPath)
    conf = yaml.load(open(helmPath,'r'))
    return conf


def handleEndpoint(url,envDir):
    print('handleEndpoint:',url,localConf,envDir)
    endpoints = localConf.get(url,None)
    if endpoints:
        for env,endpoint in endpoints.items():
            if envDir.endswith(env):
                return endpoint
        quit(f'coulnd find value for:{url}')
    return url
    

from collections import OrderedDict
from ruamel.yaml.comments import CommentedSeq
def handleK8sYaml(conf, envDir):
    #print('conf:', type(conf),conf)
    for k,v in conf.items():
        if isinstance(v, OrderedDict):
            handleK8sYaml(v, envDir)
        elif isinstance(v, CommentedSeq):
            conf[k]=[handleEndpoint(vv, envDir) for vv in v]
            # print('v',v)
            # for item in v:
            #     handleK8sYaml(item, envDir)
        elif isinstance(v, str) and ':' in v:
            conf[k]=handleEndpoint(v, envDir)
            # print(k,type(v), v)

def importHelmConf(envDir):
    data = getHelmConf(envDir)
    handleK8sYaml(data, envDir)
    output = yamlDump(data)
    print(output)
    p = Path('./config/conf.yaml')
    if p.exists():
        yesno(f"overvide: ./config/conf.yaml?")
        p.unlink()
    open(p,'w').write(output)
    print('write success')

if __name__ == '__main__':
    envDir = gargs.envDir
    try:
        importHelmConf(envDir)
    except ParseException as e:
        print(e.args)
