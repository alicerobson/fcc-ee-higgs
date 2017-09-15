from info.sampleinfo import SampleInfo, SampleInfoGraph

import fnmatch
import os

basedir = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples/'

def find_samples(dirname):
    '''Find all samples with a yaml files in dirname'''
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        if len(fnmatch.filter(filenames, '*.yaml')):
            matches.append(root)
    return matches


########################################################################
class SampleBase(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, basedirname):
        """Constructor"""
        yamls = find_samples(basedirname)
        self.infos = map(SampleInfo, yamls)
        self.graph = SampleInfoGraph(self.infos)
    
    