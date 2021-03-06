from cpyroot import *
from cpyroot.tools.style import * 
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

from tdrstyle import tdrstyle
from fcc_ee_higgs.components.ZH_Znunu import WW, ZZ, ZH

from fitter import TemplateFitter, BaseFitter, BallFitter

plot = None

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
    # hist_name = '{} : {} | {}'.format(comp.name, var, cut)
    hist_name = comp.name
    hist = TH1F(hist_name, '', *bins)
    if comp.tree != None:
        comp.tree.Project(hist.GetName(), var, cut)
    print hist_name
    return hist

def prepare_plot(var, cut, lumi):
    comps = [WW, ZZ, ZH] 
    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/analysis/ZH_nunubb/June26'

    plot = DataMCPlot('recoil', histPref)

    for comp in comps:
        load(comp, basedir)
        hist = project(comp, var, cut, *bins)    
        plot.AddHistogram(comp.name, hist)
        plot.histosDict[comp.name].SetWeight(comp.getWeight(lumi).GetWeight())
    plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
    return plot

def draw(var, cut, lumi, title=''):
    global plot
    plot = prepare_plot(var, cut, lumi)
    plot.DrawStack()
    # plot.supportHist.GetYaxis().SetRangeUser(0,2300)
    plot.supportHist.GetYaxis().SetTitleOffset(1.35)
    plot.supportHist.GetYaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetTitle(title)
    print var, cut 
    

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1

    cut = 'abs(zed_m-91)<5. && zed_pt>10 && zed_pz<50 && zed_acol>100 && zed_acop>10 \
    && (jet1_e<0 || jet1_22_e/jet1_e<0.8) && (jet2_e<0 || jet2_22_e/jet2_e<0.8) && (jet1_b==1 || jet2_b==1)'

    cut_z = '(abs(zed_m-91)<5. && zed_pt>10 && zed_pz<50 && zed_acol>100 && zed_acop>10 \
    && (jet1_e<0 || jet1_22_e/jet1_e<0.8) && (jet2_e<0 || jet2_22_e/jet2_e<0.8))'
    cut_hbb = '(jet1_b==1 || jet2_b==1)'
    cut_hinv = '(jet1_e<0 && jet2_e<0)'
    cut_hvis = 'jet1_e>0 && jet2_e>0'
    cut_missingzmass = 'misenergy_m>65 && misenergy_m<125'
    cut_haco = 'higgs_pt>10 && higgs_pz<50 && higgs_acol>100 && higgs_acop>10'

    # cut = '&&'.join([cut_z, cut_hbb])
    # cut = '&&'.join([cut_z, cut_hinv])
    cut_ZH = '&&'.join([cut_z, cut_hvis])
    cut_ZHnunubb = '&&'.join([cut_missingzmass, cut_hbb, cut_haco])
    # cut_ZHnunubb = '&&'.join([cut_missingzmass, cut_hbb])
    # cut = cut_z
    # cut = 'zed_m>50'
    bins = 50, 50, 150
    
    lumi = 5e6  # 5ab-1
    lumi = 1e6

    var = 'higgs_m'
    cut = cut_ZHnunubb

    # import pdb; pdb.set_trace()
    draw(var, cut, lumi)

##    tfitter = TemplateFitter(plot)
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
#    sys.exit(1)
##    fitter.draw_pdfs()

