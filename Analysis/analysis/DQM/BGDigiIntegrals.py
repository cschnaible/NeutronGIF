import os
import numpy as np
import ROOT as R
import Gif.Analysis.Primitives as Primitives
import Gif.Analysis.Plotter as Plotter
import Gif.Analysis.Auxiliary as Aux
import Gif.Analysis.ChamberHandler as CH
import Gif.Analysis.MegaStruct as MS
import Gif.Analysis.BGDigi as BGDigi

##### GLOBALS #####
#MS.F_MCDATA = '$WS/public/Neutron/hacktrees2/hacktree.root'
MS.F_MCDATA = '$WS/public/Neutron/ana_Neutron_MC_25000_Hack3.root'
RINGLIST  = ['11', '12', '13', '21', '22', '31', '32', '41', '42']
ERINGLIST = ['-42', '-41', '-32', '-31', '-22', '-21', '-13', '-12', '-11', '+11', '+12', '+13', '+21', '+22', '+31', '+32', '+41', '+42']
RINGDICT  = dict(zip(ERINGLIST, range(-9,0) + range(1,10)))

DOZJETS = False
DOROAD  = True
DOGAP   = True
GAP     = 35

##### FUNCTIONS #####
# runs before file loop; open a file, declare a hist dictionary
def setup(self, PARAMS):
	FN = PARAMS['OFN']
	RINGLIST = PARAMS['RINGLIST']
	self.F_OUT = R.TFile(FN,'RECREATE')
	self.F_OUT.cd()
	self.HISTS = {'comp' : {}, 'wire' : {}}
	for name in self.HISTS.keys():
		self.HISTS[name]['int'] = R.TH1F('h'+name+'int', '', 20, -10, 10)
		self.HISTS[name]['int'].SetDirectory(0)

		self.HISTS[name]['BX'] = {}
		self.HISTS[name]['time'] = {}
		self.HISTS[name]['rainbow'] = {}
		for ring in RINGLIST:
			self.HISTS[name]['BX'][ring] = {}
			for timeBin in range(0, 16):
				self.HISTS[name]['BX'][ring][timeBin] = R.TH1F('h'+name+'BX'+ring+str(timeBin), '', 50, 1, 51)
				self.HISTS[name]['BX'][ring][timeBin].SetDirectory(0)

			self.HISTS[name]['time'][ring] = {}
			for BX in range(1, 50):
				self.HISTS[name]['time'][ring][BX] = R.TH1F('h'+name+'time'+ring+str(BX), '', 16, 0, 16)
				self.HISTS[name]['time'][ring][BX].SetDirectory(0)

			#self.HISTS[name]['rainbow'][ring] = R.TH1F('h'+name+'rainbow'+ring, '', 16, 0, 16)
			self.HISTS[name]['rainbow'][ring] = R.TH2F('h'+name+'rainbow'+ring, '', 16, 0, 16, 50, 1, 51)
			self.HISTS[name]['rainbow'][ring].SetDirectory(0)

def loopFunction(self, t, PARAMS):
	TYPE = PARAMS['TYPE']
	DOZJETS = PARAMS['DOZJETS']
	DOGAP = PARAMS['DOGAP']
	DOROAD = PARAMS['DOROAD']
	GAP = PARAMS['GAP']
	RINGLIST = PARAMS['RINGLIST']
	RINGDICT = PARAMS['RINGDICT']

	if TYPE == 'P5':
		if DOZJETS:
			if      t.Z_mass <= 98. and t.Z_mass >= 84.\
				and t.nJets20 == 0\
				and t.Z_pT <= 20.:
				pass
			else:
				return

		if DOGAP:
			size, diff, train = self.getBunchInfo(t.Event_RunNumber, t.Event_BXCrossing, minSize=GAP)
			#if size not in self.COUNTS.keys():
			#	self.COUNTS[size] = 0
			#self.COUNTS[size] += 1

			if not size: return

		if list(t.lct_id) == [] or list(t.comp_id) == []: return
		E = Primitives.ETree(t, DecList=['LCT','COMP','WIRE'])
		lcts  = [Primitives.LCT    (E, i) for i in range(len(E.lct_cham ))]
		comps = [Primitives.Comp   (E, i) for i in range(len(E.comp_cham))]
		wires = [Primitives.Wire   (E, i) for i in range(len(E.wire_cham))]

		bgLCTs, bgComps = BGDigi.getBGCompCandList(lcts, comps)
		if len(bgLCTs) == 0: return # skip event if there were no isolated LCTs
		if DOROAD:
			roadChams = BGDigi.removeDigiRoads(bgComps)
		else:
			roadChams = []

		for lct, half in bgLCTs:
			# Skip Chamber if there's a background road
			if lct.cham in roadChams and DOROAD: continue
			cham = CH.Chamber(lct.cham)
			for comp in bgComps:
				if comp.cham!=lct.cham: continue
				self.HISTS['comp']['rainbow'][cham.display('{S}{R}')].Fill(comp.timeBin, diff)
				self.HISTS['comp']['BX'][cham.display('{S}{R}')][comp.timeBin].Fill(diff)
				if diff < 50:
					self.HISTS['comp']['time'][cham.display('{S}{R}')][diff].Fill(comp.timeBin)
				if comp.timeBin >= 1 and comp.timeBin <= 5 and diff == 1:
					self.HISTS['comp']['int'].Fill(RINGDICT[cham.display('{E}{S}{R}')])

		bgLCTs, bgWires = BGDigi.getBGWireCandList(lcts,wires)
		if len(bgLCTs) == 0: return # skip event if no isolated LCTs
		if DOROAD:
			roadChams = BGDigi.removeDigiRoads(bgWires)
		else:
			roadChams = []

		for lct, half in bgLCTs:
			# skip chamber if there's a background track
			if lct.cham in roadChams and DOROAD: continue
			cham = CH.Chamber(lct.cham)
			for wire in bgWires:
				if wire.cham != lct.cham: continue
				self.HISTS['wire']['rainbow'][cham.display('{S}{R}')].Fill(wire.timeBin, diff)
				self.HISTS['wire']['BX'][cham.display('{S}{R}')][wire.timeBin].Fill(diff)
				if diff < 50:
					self.HISTS['wire']['time'][cham.display('{S}{R}')][diff].Fill(wire.timeBin)
				if wire.timeBin >= 1 and wire.timeBin <= 5 and diff == 1:
					self.HISTS['wire']['int'].Fill(RINGDICT[cham.display('{E}{S}{R}')])

	elif TYPE == 'MC':
		E = Primitives.ETree(t, DecList=['COMP','WIRE'])
		comps = [Primitives.Comp   (E, i) for i in range(len(E.comp_cham))]
		wires = [Primitives.Wire   (E, i) for i in range(len(E.wire_cham))]

		for comp in comps:
			cham = CH.Chamber(comp.cham)
			if comp.timeBin < 10: continue
			self.HISTS['comp']['int'].Fill(RINGDICT[cham.display('{E}{S}{R}')])

		for wire in wires:
			if wire.timeBin < 12: continue
			cham = CH.Chamber(comp.cham)
			self.HISTS['wire']['int'].Fill(RINGDICT[cham.display('{E}{S}{R}')])

def writeHistos(self, PARAMS):
	RINGLIST = PARAMS['RINGLIST']
	self.F_OUT.cd()
	for name in self.HISTS.keys():
		self.HISTS[name]['int'].Write()
		for ring in RINGLIST:
			for timeBin in range(0, 16):
				self.HISTS[name]['BX'][ring][timeBin].Write()
			for BX in range(1, 50):
				self.HISTS[name]['time'][ring][BX].Write()
			self.HISTS[name]['rainbow'][ring].Write()

# once per file
def analyze(self, t, PARAMS):
	TYPE = PARAMS['TYPE']
	if TYPE == 'P5':
		Primitives.SelectBranches(t, DecList=['LCT','COMP','WIRE'], branches=['Z_mass','Z_pT','nJets20', 'Event_RunNumber', 'Event_BXCrossing'])
	elif TYPE == 'MC':
		Primitives.SelectBranches(t, DecList=['COMP','WIRE'])
	for idx, entry in enumerate(t):
	#for idx in xrange(START, END+1)
		if idx == 1000: break
		#t.GetEntry(idx)
		print 'Events:', idx+1, '\r',
		loopFunction(self, t, PARAMS)

	writeHistos(self, PARAMS)

# if file is already made
def load(self, PARAMS):
	RINGLIST = PARAMS['RINGLIST']
	f = R.TFile.Open(self.F_DATAFILE)
	self.HISTS = {}
	self.HISTS = {'comp' : {}, 'wire' : {}}
	for name in self.HISTS.keys():
		self.HISTS[name]['int'] = f.Get('h'+name+'int')
		self.HISTS[name]['int'].SetDirectory(0)

		self.HISTS[name]['BX'] = {}
		self.HISTS[name]['time'] = {}
		self.HISTS[name]['rainbow'] = {}
		for ring in RINGLIST:
			self.HISTS[name]['BX'][ring] = {}
			for timeBin in range(0, 16):
				self.HISTS[name]['BX'][ring][timeBin] = f.Get('h'+name+'BX'+ring+str(timeBin))
				self.HISTS[name]['BX'][ring][timeBin].SetDirectory(0)

			self.HISTS[name]['time'][ring] = {}
			for BX in range(1, 50):
				self.HISTS[name]['time'][ring][BX] = f.Get('h'+name+'time'+ring+str(BX))
				self.HISTS[name]['time'][ring][BX].SetDirectory(0)

			#self.HISTS[name]['rainbow'][ring] = f.Get('h'+name+'rainbow'+ring)
			self.HISTS[name]['rainbow'][ring] = f.Get('h'+name+'rainbow'+ring)
			self.HISTS[name]['rainbow'][ring].SetDirectory(0)
	
def cleanup(self, PARAMS):
	pass
	print ''

##### MAKEPLOT FUNCTIONS #####
def makeIntegralsPlot(h, DIGI, ERINGLIST, RINGDICT):
	plot = Plotter.Plot(h, option='hist')

	canvas = Plotter.Canvas(lumi='Background {DIGI} by Ring, {TYPE}'.format(DIGI='Comparators' if DIGI=='comp' else 'Wires', TYPE=TYPE), cWidth=1000)

	canvas.addMainPlot(plot)

	canvas.makeTransparent()
	h.GetXaxis().SetRangeUser(-9,10)
	for ring in ERINGLIST:
		bin_ = RINGDICT[ring] + 11
		h.GetXaxis().SetBinLabel(bin_, ring.replace('-','#minus'))
	plot.SetLineColor(0)
	plot.SetFillColor(R.kOrange)
	plot.scaleLabels(1.25, 'X')
	plot.setTitles(X='CSC Ring', Y='Counts')
	plot.SetMinimum(0)

	canvas.finishCanvas()
	canvas.save('pdfs/Integral_{DIGI}_{TYPE}.pdf'.format(DIGI=DIGI,TYPE=TYPE))
	R.SetOwnership(canvas, False)
	canvas.deleteCanvas()

def makeBX15Plot(hdict, DIGI, RING):
	h = hdict[DIGI]['BX'][RING][1].Clone()
	for timeBin in range(1, 6):
		h.Add(hdict[DIGI]['BX'][RING][timeBin])

	plot = Plotter.Plot(h, option='hist')

	canvas = Plotter.Canvas(lumi='BG {DIGI} in ME{RING} vs. BX After Gap'.format(
		DIGI='Comparators' if DIGI=='comp' else 'Wires',
		RING=RING,
	))

	canvas.addMainPlot(plot)
	canvas.makeTransparent()
	plot.SetLineColor(0)
	plot.SetFillColor(R.kOrange)
	plot.setTitles(X='BX After Gap', Y='Counts')
	plot.SetMinimum(0)

	canvas.finishCanvas()
	canvas.save('pdfs/BX_{DIGI}_{RING}.pdf'.format(DIGI=DIGI, RING=RING))
	R.SetOwnership(canvas, False)
	canvas.deleteCanvas()

def makeTimePlot(h, DIGI, RING, BX):
	plot = Plotter.Plot(h, option='hist')

	canvas = Plotter.Canvas(lumi='BG {DIGI} in ME{RING} vs. Time Bin, BX {BX}'.format(
		DIGI='Comparators' if DIGI=='comp' else 'Wires',
		RING=RING,
		BX=BX
	))

	canvas.addMainPlot(plot)
	canvas.makeTransparent()
	plot.SetLineColor(0)
	plot.SetFillColor(R.kOrange)
	plot.setTitles(X='Time Bin', Y='Counts')
	plot.SetMinimum(0)
	#plot.SetMaximum(700)

	canvas.finishCanvas()
	canvas.save('pdfs/TimeBin_{DIGI}_{RING}_{BX}.pdf'.format(DIGI=DIGI, RING=RING, BX=BX))
	R.SetOwnership(canvas, False)
	canvas.deleteCanvas()

def makeBXPlot(h, DIGI, RING, TB):
	plot = Plotter.Plot(h, option='hist')

	canvas = Plotter.Canvas(lumi='BG {DIGI} in ME{RING} vs. BX After Gap, Time Bin {TB}'.format(
		DIGI='Comps' if DIGI=='comp' else 'Wires',
		RING=RING,
		TB=TB
	))

	canvas.addMainPlot(plot)
	canvas.makeTransparent()
	plot.SetLineColor(0)
	plot.SetFillColor(R.kOrange)
	plot.setTitles(X='BX After Gap', Y='Counts')
	plot.SetMinimum(0)
	#plot.SetMaximum(1400)

	canvas.finishCanvas()
	canvas.save('pdfs/BX_{DIGI}_{RING}_{TB}.pdf'.format(DIGI=DIGI, RING=RING, TB=TB))
	R.SetOwnership(canvas, False)
	canvas.deleteCanvas()

def makeRainbowPlot(h, DIGI, RING):
	plot = Plotter.Plot(h, option='colz')

	canvas = Plotter.Canvas(lumi='BX After Gap vs. Time Bin: {DIGI}, ME{RING}'.format(
		DIGI='Comparators' if DIGI=='comp' else 'Wires',
		RING=RING,
	))

	canvas.addMainPlot(plot)
	canvas.makeTransparent()
	#plot.SetLineColor(0)
	plot.SetFillColor(R.kOrange)
	plot.setTitles(X='Time Bin', Y='BX After Gap')
	plot.SetMinimum(0)
	canvas.scaleMargins(1.7, 'R')

	canvas.finishCanvas()
	canvas.save('pdfs/Rainbow_{DIGI}_{RING}.pdf'.format(DIGI=DIGI, RING=RING))
	R.SetOwnership(canvas, False)
	canvas.deleteCanvas()

##### ACTUAL CODE TO RUN #####
if __name__ == '__main__':
	#### SETUP SCRIPT #####
	# Output file names
	CONFIG = {
		'P5'  : 'Integrals_P5.root',
		'MC'  : 'Integrals_MC.root'
	}
	# Set module globals: TYPE=[GIF/P5/MC], OFN=Output File Name, FDATA=[OFN/None]
	TYPE, OFN, FDATA = MS.ParseArguments(CONFIG)

	##### DECLARE ANALYZERS AND RUN ANALYSIS #####
	R.gROOT.SetBatch(True)
	R.gStyle.SetPalette(55)
	R.gStyle.SetNumberContours(100)
	METHODS = ['analyze', 'load', 'setup', 'cleanup']
	ARGS = {
		'PARAMS' : {
			'OFN':OFN,
			'TYPE':TYPE,
			'DOZJETS':DOZJETS,
			'DOROAD':DOROAD,
			'DOGAP':DOGAP,
			'GAP':GAP,
			'RINGLIST':RINGLIST,
			'RINGDICT':RINGDICT,
		},
		'F_DATAFILE' : FDATA
	}
	if TYPE == 'GIF':
		ARGS['ATTLIST'] = [float('inf')]
	Analyzer = getattr(MS, TYPE+'Analyzer')
	for METHOD in METHODS:
		setattr(Analyzer, METHOD, locals()[METHOD])
	data = Analyzer(**ARGS)

	##### MAKE PLOTS #####
	for DIGI in data.HISTS.keys():
		makeIntegralsPlot(data.HISTS[DIGI]['int'], DIGI, ERINGLIST, RINGDICT)
		if TYPE == 'P5':
			for RING in RINGLIST:
				makeRainbowPlot(data.HISTS[DIGI]['rainbow'][RING], DIGI, RING)
				makeBX15Plot(data.HISTS, DIGI, RING)

				for TB in range(0, 16):
					makeBXPlot(data.HISTS[DIGI]['BX'][RING][TB], DIGI, RING, TB)
				for BX in range(1, 50):
					makeTimePlot(data.HISTS[DIGI]['time'][RING][BX], DIGI, RING, BX)
