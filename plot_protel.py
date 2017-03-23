#!/usr/bin/env python
'''
    A python script creates Protel plot files to build a board:
'''

import sys

from pcbnew import *
project=sys.argv[1]
revision=sys.argv[2]
filename=project + ".kicad_pcb"
GerberDir = "./Revision/" + revision + "/" + project + "/TR/GERBER/"
ProtelDir = "./Revision/" + revision + "/" + project + "/TR/PROTEL/"
DrillDir = "./Revision/" + revision + "/" + project + "/TR/DRILL/"
DocDir = "./Revision/" + revision + "/" + project + "/Documents/"

board = LoadBoard(filename)
pctl = PLOT_CONTROLLER(board)
popt = pctl.GetPlotOptions()
popt.SetOutputDirectory(ProtelDir)

# Set some important plot options:
popt.SetPlotFrameRef(False)
popt.SetAutoScale(False)
popt.SetMirror(False)
popt.SetUseGerberAttributes(True)
popt.SetUseGerberProtelExtensions(True)
popt.SetExcludeEdgeLayer(True);
popt.SetUseAuxOrigin(True)
popt.SetPlotValue(False)
popt.SetPlotReference(False)
popt.SetSubtractMaskFromSilk(False)
popt.SetScale(1)
popt.SetLineWidth(FromMM(0.35))

plot_plan = [
    ( "CuTop", F_Cu, "Top layer" ),
    ( "CuBottom", B_Cu, "Bottom layer" ),
    ( "PasteBottom", B_Paste, "Paste Bottom" ),
    ( "PasteTop", F_Paste, "Paste top" ),
    ( "SilkTop", F_SilkS, "Silk top" ),
    ( "SilkBottom", B_SilkS, "Silk top" ),
    ( "MaskBottom", B_Mask, "Mask bottom" ),
    ( "MaskTop", F_Mask, "Mask top" ),
    ( "EdgeCuts", Edge_Cuts, "Edges" ),
]

for layer_info in plot_plan:
    pctl.SetLayer(layer_info[1])
    pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
    print 'plot %s' % pctl.GetPlotFileName()
    if pctl.PlotLayer() == False:
        print "plot error"

#generate internal copper layers, if any
lyrcnt = board.GetCopperLayerCount();

for innerlyr in range ( 1, lyrcnt-1 ):
    pctl.SetLayer(innerlyr)
    lyrname = 'inner%s' % innerlyr
    pctl.OpenPlotfile(lyrname, PLOT_FORMAT_GERBER, "inner")
    print 'plot %s' % pctl.GetPlotFileName()
    if pctl.PlotLayer() == False:
        print "plot error"

pctl.ClosePlot()
