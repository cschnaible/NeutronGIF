import numpy as np
import ROOT as R
import Gif.Analysis.Primitives as Primitives
import Gif.Analysis.Auxiliary as Aux
import DisplayHelper as ED # "Event Display"
import Patterns
import argparse
import Gif.Analysis.ChamberHandler as CH

##########
# This file gets the data, makes the histograms, makes the objects, and makes the plots
# It is the true meat of the analysis; anything cosmetic or not directly relevant should
# be moved to one of the other files: Primitives for classes, DisplayHelper for cosmetics
##########

R.gROOT.SetBatch(True)
ED.setStyle('rechits') # holy crap! setStyle was taking up 99% of the computation time!

##### COMMAND LINE PARAMETERS
parser = argparse.ArgumentParser(description='Makes event displays')
parser.add_argument('--config',dest='CONFIG',help='Configuration file'   ,default='ED.config')
parser.add_argument('--outDir',dest='OUTDIR',help='Plot saving directory',default='pdfs'     )
args = parser.parse_args()

##### PARAMETERS #####
OUTDIR = args.OUTDIR
# CONFIG dictionary: CONFIG[FN][ENTRY] = [CHAMLIST]
CONFIG = {}
F_CONFIG = open(args.CONFIG)
for line in F_CONFIG:
	# skip empty lines and comments
	if line[0] == '#' or line == '\n':
		continue
	cols = line.strip('\n').split()
	if cols[0] == 'GIF':
		MEAS = cols[1]
		FN = '../../trees/ana_'+MEAS+'.root'
		CONFIG[FN] = {}
	elif cols[0] == 'P5':
		FN = cols[1]
		CONFIG[FN] = {}
	else:
		ENTRY = int(cols[0])
		CHAM  = int(cols[1])
		if ENTRY not in CONFIG[FN].keys():
			CONFIG[FN][ENTRY] = []
		CONFIG[FN][ENTRY].append(CHAM)

# Which displays to plot
DOSEGMENTS = True
DRAWZTITLE = False
TITLESON   = True
ORIGFORMAT = False

##### BEGIN CODE #####

for FILE in CONFIG.keys():
	# Get file and tree
	f = R.TFile.Open(FILE)
	t = f.Get('GIFTree/GIFDigiTree')

	for ENTRY in CONFIG[FILE].keys():
		# Get the event, make the ETree, and make lists of primitives objects
		t.GetEntry(ENTRY)
		EVENT = t.Event_EventNumber
		DecList = ['RECHIT']
		if DOSEGMENTS:
			DecList.extend(['SEGMENT', 'LCT'])

		E = Primitives.ETree(t, DecList)
		rechits = [Primitives.RecHit (E, i) for i in range(len(E.rh_cham   ))]
		if DOSEGMENTS:
			segs    = [Primitives.Segment(E, i) for i in range(len(E.seg_cham  ))]
			lcts    = [Primitives.LCT    (E, i) for i in range(len(E.lct_cham  ))]

		for CHAM in CONFIG[FILE][ENTRY]:
			CHAMBER = CH.Chamber(CHAM)
			# Upper limits for wire group numbers and half strip numbers

			##### RECHITS DISPLAY #####
			WIRE_MAX = CHAMBER.nwires
			HS_MAX   = CHAMBER.nstrips*2

			# Ndivisions codes
			ND = {\
				'st' : { 64 : 520,  80 : 520, 112 : 1020            },
				'wg' : { 48 : 520,  64 : 520,  96 :  520, 112 : 1020}
			}

			# Instantiate canvas
			canvas = ED.Canvas('rechits' if not ORIGFORMAT else 'origrechits')

			rhL = { 'all' : [8.                ], 'seg' : [8.                ]}
			rhS = { 'all' : [float(HS_MAX)     ], 'seg' : [float(HS_MAX)     ]}
			rhW = { 'all' : [float(WIRE_MAX+10)], 'seg' : [float(WIRE_MAX+10)]}
			for rh in rechits:
				if rh.cham != CHAM: continue
				rhS['all'].append(float(rh.halfStrip)/2.+ 0.5)
				rhW['all'].append(float(rh.wireGroup)   + 0.5)
				rhL['all'].append(float(rh.layer)       + 0.5)

			gRHS = R.TGraph(len(rhS['all']), np.array(rhS['all']), np.array(rhL['all']))
			canvas.pads[0].cd()
			gRHS.Draw('AP')
			gRHS.SetMarkerColor(R.kBlack)
			gRHS.GetXaxis().SetNdivisions(ND['st'][HS_MAX/2])
			gRHS.SetTitle(('' if not TITLESON else 'RECHIT STRIPS')+';Strip Number;Layer'+('' if not DRAWZTITLE else ';Multiplicity'))
			gRHS.SetMinimum(1.)
			gRHS.SetMaximum(7.)
			gRHS.GetXaxis().SetLimits(1., HS_MAX/2+1.)
			gRHS.Draw('AP')
			canvas.canvas.Update()

			gRHW = R.TGraph(len(rhW['all']), np.array(rhW['all']), np.array(rhL['all']))
			canvas.pads[2 if not ORIGFORMAT else 1].cd()
			gRHW.Draw('AP')
			gRHW.SetMarkerColor(R.kBlack)
			gRHW.GetXaxis().SetNdivisions(ND['wg'][WIRE_MAX])
			gRHW.SetTitle(('' if not TITLESON else 'RECHIT WIRE GROUPS')+';Wire Group Number;Layer'+('' if not DRAWZTITLE else ';Multiplicity'))
			gRHW.SetMinimum(1.)
			gRHW.SetMaximum(7.)
			gRHW.GetXaxis().SetLimits(1., WIRE_MAX+1.)
			gRHW.Draw('AP')
			canvas.canvas.Update()

			# Segments
			if DOSEGMENTS:
				SegDrawList = []
				for seg in segs:
					if seg.cham != CHAM: continue
					for lct in lcts:
						if lct.cham != CHAM: continue
						if Aux.matchSegLCT(seg, lct, thresh=(2., 2.), old=False):
							SegDrawList.append(seg)
				SEGLAYERS = [1, 2, 3, 4, 5, 6]
				layZ = np.array([float(i) + 0.5 for i in SEGLAYERS])
				segGraphs = []
				for seg in SegDrawList:
					for i in seg.rhID:
						rhS['seg'].append(float(rechits[i].halfStrip)/2.+ 0.5)
						rhW['seg'].append(float(rechits[i].wireGroup)   + 0.5)
						rhL['seg'].append(float(rechits[i].layer)       + 0.5)
					segGraphs.append({})
					stX = np.array([seg.staggeredStrip    [lay]+1.0 for lay in SEGLAYERS])
					wgX = np.array([seg.wireGroup         [lay] for lay in SEGLAYERS])
					segGraphs[-1]['st'] = {'fill' : R.TGraph(len(layZ), stX, layZ), 'empt' : R.TGraph(len(layZ), stX, layZ), 'pad' : 0}
					segGraphs[-1]['wg'] = {'fill' : R.TGraph(len(layZ), wgX, layZ), 'empt' : R.TGraph(len(layZ), wgX, layZ), 'pad' : 2}

				gSRHS = R.TGraph(len(rhS['seg']), np.array(rhS['seg']), np.array(rhL['seg']))
				canvas.pads[0].cd()
				gSRHS.Draw('P')
				gSRHS.SetMarkerColor(R.kRed)
				gSRHW = R.TGraph(len(rhW['seg']), np.array(rhW['seg']), np.array(rhL['seg']))
				canvas.pads[2 if not ORIGFORMAT else 1].cd()
				gSRHW.Draw('P')
				gSRHW.SetMarkerColor(R.kRed)

				for gr in segGraphs:
					for key in ['st', 'wg']:
						gr[key]['fill'].SetMarkerColor(R.kWhite)
						gr[key]['fill'].SetMarkerStyle(R.kFullCircle)
						gr[key]['empt'].SetMarkerColor(R.kBlack)
						gr[key]['empt'].SetMarkerStyle(R.kOpenCircle)
						for which in ['fill', 'empt']:
							gr[key][which].SetMarkerSize(1)
							gr[key][which].SetLineWidth(3)
							gr[key][which].SetLineColor(R.kBlue)
						canvas.pads[gr[key]['pad']].cd()
						gr[key]['fill'].Draw('L same')
						gr[key]['empt'].Draw('L same')

			##### CLEAN UP #####
			for pad in canvas.pads:
				pad.cd()
				pad.RedrawAxis()

			# lumi text
			RUN = t.Event_RunNumber
			LS  = t.Event_LumiSection
			canvas.drawLumiText(CHAMBER.display('ME{E}{S}/{R}/{C}') + ', REL =({R},{E},{L})'.format(R=str(RUN),E=str(EVENT),L=str(LS)))

			# save as
			canvas.canvas.SaveAs(OUTDIR+'/RH_'+CHAMBER.display('ME{E}{S}{R}{C}_')+str(EVENT)+'.pdf')
			R.SetOwnership(canvas.canvas, False)
			print '\033[1mFILE \033[32m'+'RH_'+CHAMBER.display('ME{E}{S}{R}{C}_')+str(EVENT)+'.pdf'+'\033[30m CREATED\033[0m'

			del gRHS, gRHW
			canvas.deleteCanvas()

	f.Close()
