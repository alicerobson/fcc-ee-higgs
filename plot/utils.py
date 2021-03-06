from cpyroot import *

from cpyroot.tools.style import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot


histPref = {
    'ZZ*': {'style':sBlue, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sRed, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sGreen, 'layer':11, 'legend':'ZH'},
}

def load(comp, basedir):
    comp.directory = '/'.join([basedir, comp.name])
    print comp.directory
    comp.rootfile = TFile('{}/{}'.format(
        comp.directory,
        'heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root'
    ))
    comp.tree = comp.rootfile.Get('events')
    print comp
    print '-'
    
    
def project(comp, var, cut, *bins):
    hist_name = comp.name
    hist = TH1F(hist_name, '', *bins)
    if comp.tree != None:
        comp.tree.Project(hist.GetName(), var, cut)
    print hist_name
    return hist

def prepare_plot(var, cut, bins, lumi, comps, basedir):
    plot = DataMCPlot('recoil', histPref)
    for comp in comps:
        load(comp, basedir)
        hist = project(comp, var, cut, *bins)    
        plot.AddHistogram(comp.name, hist)
        plot.histosDict[comp.name].SetWeight(comp.getWeight(lumi).GetWeight())
    plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
    return plot

def draw(var, cut, bins, lumi, comps, basedir, title=''):
    global plot
    plot = prepare_plot(var, cut, bins, lumi, comps, basedir)
    plot.DrawStack()
    plot.supportHist.GetYaxis().SetTitleOffset(1.35)
    plot.supportHist.GetYaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetTitle(title)
    print var, cut 
    
