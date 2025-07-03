from setuptools import setup,find_packages
from typing import List

def get_req()->List[str]:
    require_lst:List[str]=[]
    try:
        with open('requirements.txt', 'r') as f:
            lines=f.readlines()
            for line in lines:
                req = line.strip()
                if req and req!='-e .':
                    require_lst.append(req)
    except FileNotFoundError:
        print("No requirements.txt file found")
    return require_lst
setup(
    name='NetSec',
    version='1.0.0',
    packages=find_packages(),
    install_requires=get_req(),
    author='Raghav Mittal',
)

        