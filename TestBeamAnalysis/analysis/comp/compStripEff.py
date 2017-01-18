''' Purpose of this script is to measure the Comp efficiency.
Efficiency is defined as given ADC count data on a specific strip and layer 
near a LCT pattern, what is the probability that there is a 
Comp made at the location of strip ADC data'''

import numpy as np
import ROOT as R
import Gif.TestBeamAnalysis.Primitives as Primitives
import Gif.TestBeamAnalysis.Plotter as Plotter
import Gif.TestBeamAnalysis.Auxiliary as Aux

##### PARAMETERS #####
# Which chambers to do
CHAMLIST = (1, 110)

##### SEMI-PARAMETERS #####
# Filenames
F_MEASGRID = '../datafiles/measgrid'
F_ATTENHUT = '../datafiles/attenhut'
#F_DATAFILE = '../datafiles/data_compStripEff'
F_DATAFILE = 'data_compStripEff'
#F_DATAFILE = None

# Cosmetic data dictionary, comment out for fewer ones
pretty = {
	0 : { 'name' : 'Original',        'color' : R.kRed-3,   'marker' : R.kFullCircle      },
	1 : { 'name' : 'TightPreCLCT',    'color' : R.kBlue-1,  'marker' : R.kFullSquare      },
	2 : { 'name' : 'TightCLCT',       'color' : R.kOrange,  'marker' : R.kFullTriangleUp  },
	3 : { 'name' : 'TightALCT',       'color' : R.kGreen+2, 'marker' : R.kFullCross       },
	4 : { 'name' : 'TightPrePID',     'color' : R.kMagenta, 'marker' : R.kFullTriangleDown},
	5 : { 'name' : 'TightPrePostPID', 'color' : R.kAzure+8, 'marker' : R.kFullDiamond     },
	6 : { 'name' : 'TightPA',         'color' : R.kGray,    'marker' : R.kFullStar        },
	7 : { 'name' : 'TightAll',        'color' : R.kBlack,   'marker' : R.kFullCircle      }
}

##### BEGIN CODE #####
R.gROOT.SetBatch(True)

##### MEGASTRUCT CLASS #####
class MegaStruct():
	#### BEGIN MEGASTRUCT COMMON: DO NOT EDIT BETWEEN THESE TAGS #####
	def __init__(self):
		self.fillMeas()
		self.fillCurr()
		self.fillData()
	
	# general fill measurement data function
	def fillMeas(self):
		f = open(F_MEASGRID)
		self.MEASDATA = {}
		for line in f:
			cols = line.strip('\n').split()
			self.MEASDATA[float(cols[0])] = [int(j) for j in cols[1:]]
		f.close()

	# general fill current data function
	def fillCurr(self):
		f = open(F_ATTENHUT)
		self.CURRDATA = { 1 : {}, 110: {} }
		currentCham = 1
		for line in f:
			if line == '\n':
				currentCham = 110
				continue
			cols = line.strip('\n').split()
			currentMeas = int(cols[1])
			self.CURRDATA[currentCham][currentMeas] = [float(i) for i in cols[2:]]
		f.close()

	# get a current measurement given a chamber and measurement number
	def current(self, cham, meas):
		if cham == 1:
			return sum(self.CURRDATA[cham][meas])/6.0
		elif cham == 110:
			return sum(self.CURRDATA[cham][meas][6:12])/6.0
	
	# get a vector of attenuations
	def attVector(self, castrated=False):
		if castrated: # for comparing to Yuriy
			return np.array([33., 46., 100., float('inf')])
		else:
			return np.array(sorted(self.MEASDATA.keys()))

	# get a vector of currents
	def currentVector(self, cham, ff, castrated=False):
		return np.array([self.current(cham, self.MEASDATA[att][ff]) for att in self.attVector(castrated)])

	# get a vector of equivalent luminosities
	def lumiVector(self, cham, ff, castrated=False):
		factor = 3.e33 if cham == 1 else 5.e33
		return factor * np.array([self.current(cham, self.MEASDATA[att][ff]) for att in self.attVector(castrated)])
	##### END MEGASTRUCT COMMON: DO NOT EDIT BETWEEN THESE TAGS #####

	# fill data: this function, and the access functions below it, are "user-defined" and script-dependent
	def fillData(self):
		# fill a data dictionary as desired
		self.numerator = { 1 : {}, 110: {} }
		self.denominator = { 1 : {}, 110: {} }
		if F_DATAFILE is None:
			for ATT in self.MEASDATA.keys():
				for MEAS in self.MEASDATA[ATT]:
					for cham in CHAMLIST:
						self.numerator[cham][MEAS] = 0
						self.denominator[cham][MEAS] = 0
					f = R.TFile.Open('../../trees/ana_'+str(MEAS)+'.root')
					t = f.Get('GIFTree/GIFDigiTree')
					DecList = ['STRIP','WIRE','COMP','LCT','CLCT']
					for entry in t:
						E = Primitives.ETree(t,DecList)
						strips = [Primitives.Strip(E,i) for i in range(len(E.strip_cham))]
						wires  = [Primitives.Wire(E,i)  for i in range(len(E.wire_cham))]
						comps  = [Primitives.Comp(E,i)  for i in range(len(E.comp_cham))]
						lcts   = [Primitives.LCT(E,i)   for i in range(len(E.lct_cham))]
						for cham in CHAMLIST:
							# Require the presence of wire group and strip data and an LCT
							if cham not in [lct.cham for lct in lcts]: continue
							if cham not in [wire.cham for wire in wires]: continue
							if cham not in [strip.cham for strip in strips]: continue
							# Begin looping on LCTs to find the muon
							for lct in lcts:
								if lct.cham is not cham: continue
								stripsNearLCT = {1:[],2:[],3:[],4:[],5:[],6:[]}
								compsInLCT    = {1:[],2:[],3:[],4:[],5:[],6:[]}
								# Loop on strips to find ones close to a LCT
								for strip in strips:
									if strip.cham is not cham: continue
									# Need maximum pedestal corrected adc count to be above threshold
									ped = float(strip.ADC[0]+strip.ADC[1])/2
									if max([adc-ped for adc in strip.ADC[2:]]) > 13.3: 
										if self.stripNearLCT(strip,lct): 
											# append strip number info per layer
											stripsNearLCT[strip.layer].append(strip.number)
								# Loop on comparators to find ones close to a LCT
								for comp in comps:
									if comp.cham is not cham: continue
									if Aux.inLCTPattern(lct,comp):
										# append strip number info per layer
										compsInLCT[comp.layer].append(int(comp.strip))
								# Determine if a strip and comparator are near each other on a per layer basis
								for lay in stripsNearLCT.keys():
									# Need at least one strip to make a comparator
									if len(stripsNearLCT[lay])>0:
										# Add to denominator since there's a layer with strip data
										self.denominator[cham][MEAS] += 1
										for compStripInLCT in compsInLCT[lay]:
											if compStripInLCT in stripsNearLCT[lay]:
												# Add to numerator for each layer that has a comp near strip data
												self.numerator[cham][MEAS] += 1

					print MEAS,ATT,
					print self.numerator[1][MEAS], self.denominator[1][MEAS],
					print self.numerator[110][MEAS], self.denominator[110][MEAS]

		# for obtaining data dictionary from a file
		else:
			f = open(F_DATAFILE)
			for line in f:
				cols = line.strip('\n').split()
				MEAS = int(cols[0])
				self.numerator[1][MEAS] = float(cols[2])
				self.denominator[1][MEAS] = float(cols[3])
				self.numerator[110][MEAS] = float(cols[4])
				self.denominator[110][MEAS] = float(cols[5])

	def stripNearLCT(self,strip,lct):
		# Purpose is to find out if a given strip is in/near to an LCT pattern
		# Near is defined as the adjacent strip to a strip with a pattern
		id_ = lct.pattern
		khs = lct.keyHalfStrip
		stripHS = strip.staggeredNumber * 2

		if id_ == 2:
			pat = {6:[khs-5, khs-4, khs-3], 5:[khs-4, khs-3, khs-2], 4:[khs-2, khs-1, khs], 3:[khs], 2:[khs+1, khs+2], 1:[khs+3, khs+4, khs+5]}
		elif id_ == 3:
			pat = {1:[khs-5, khs-4, khs-3], 2:[khs-2, khs-1], 3:[khs], 4:[khs, khs+1, khs+2], 5:[khs+2, khs+3, khs+4], 6:[khs+3, khs+4, khs+5]}
		elif id_ == 4:
			pat = {6:[khs-4, khs-3, khs-2], 5:[khs-4, khs-3, khs-2], 4:[khs-2, khs-1], 3:[khs], 2:[khs+1, khs+2], 1:[khs+2, khs+3, khs+4]}
		elif id_ == 5:
			pat = {1:[khs-4, khs-3, khs-2], 2:[khs-2, khs-1], 3:[khs], 4:[khs+1, khs+2], 5:[khs+2, khs+3, khs+4], 6:[khs+2, khs+3, khs+4]}
		elif id_ == 6:
			pat = {6:[khs-3, khs-2, khs-1], 5:[khs-2, khs-1], 4:[khs-1, khs], 3:[khs], 2:[khs, khs+1], 1:[khs+1, khs+2, khs+3]}
		elif id_ == 7:
			pat = {1:[khs-3, khs-2, khs-1], 2:[khs-1, khs], 3:[khs], 4:[khs, khs+1], 5:[khs+1, khs+2], 6:[khs+1, khs+2, khs+3]}
		elif id_ == 8:
			pat = {6:[khs-2, khs-1, khs], 5:[khs-2, khs-1, khs], 4:[khs-1, khs], 3:[khs], 2:[khs, khs+1], 1:[khs, khs+1, khs+2]}
		elif id_ == 9:
			pat = {1:[khs-2, khs-1, khs], 2:[khs-1, khs], 3:[khs], 4:[khs, khs+1], 5:[khs, khs+1, khs+2], 6:[khs, khs+1, khs+2]}
		elif id_ == 10:
			pat = {6:[khs-1, khs, khs+1], 5:[khs-1, khs, khs+1], 4:[khs], 3:[khs], 2:[khs], 1:[khs-1, khs, khs+1]}

		lay = pat[strip.layer]
		lower = lay[ 0]-2 if lay[ 0]%2==0 else lay[ 0]-3
		upper = lay[-1]+3 if lay[-1]%2==0 else lay[-1]+2
		if lower <= stripHS and stripHS <= upper:
			return True
		else: 
			return False

	# Not used
	def compNearStrip(self,comp,stripsNearLCT):
		if len(stripsNearLCT[comp.layer])==0: 
			return False
		if int(comp.strip) in stripsNearLCT[comp.layer]:
			return True

	# get a value given a chamber and measurement number
	def eff(self, cham, meas):
		return float(self.numerator[cham][meas]/self.denominator[cham][meas])

	# get a vector of values
	def effVector(self, cham, ff):
		return np.array([self.eff(cham, self.MEASDATA[att][ff]) for att in self.attVector()])

data = MegaStruct()

##### MAKEPLOT FUNCTION #####
def makePlot(cham, x, y, xtitle, ytitle, title):
	graphs = []
	ntypes = len(pretty.keys())
	for i in range(ntypes):
		graphs.append(R.TGraph(len(x[i]), x[i], y[i]))

	# Step 1
	plots = []
	for i, p in enumerate(pretty.keys()):
		plots.append(Plotter.Plot(graphs[i], legName=pretty[p]['name'], legType='p', option='AP' if i==0 else 'P'))

	# Step 2
	canvas = Plotter.Canvas(lumi='ME'+str(cham)+'/1 External Trigger', logy=False, extra='Internal', cWidth=800, cHeight=700)

	# Step 3
	canvas.makeLegend(lWidth=0.2, lHeight=0.25, pos='bl', lOffset=0.04, fontsize=0.03)

	# Step 4
	for i in range(ntypes):
		canvas.addMainPlot(plots[i], isFirst=(i==0), addToLegend=True)

	# Step 5
	R.TGaxis.SetExponentOffset(-0.08, 0.02, "y")
	plots[0].setTitles(X=xtitle, Y=ytitle)
	graphs[0].SetMinimum(0.0)
	graphs[0].SetMaximum(1.1)
	plots[0].scaleTitles(0.8)
	plots[0].scaleLabels(0.8)
	plots[0].scaleTitleOffsets(1.2, 'Y')
	canvas.makeTransparent()

	for i,p in enumerate(pretty.keys()):
		graphs[i].SetMarkerColor(pretty[p]['color'])
		graphs[i].SetMarkerStyle(pretty[p]['marker'])
		graphs[i].SetMarkerSize(2.2)

	# Step 6

	# Step 7

	# Step 8
	canvas.finishCanvas()
	canvas.c.SaveAs('test/compStripEff_ME'+str(cham)+'1_'+title+'.pdf')
	R.SetOwnership(canvas.c, False)

##### MAKE PLOTS #####
for cham in CHAMLIST:
	makePlot(\
		cham if cham == 1 else 2,
		[data.lumiVector(cham, ff) for ff in pretty.keys()],
		[data.effVector (cham, ff) for ff in pretty.keys()],
		'Luminosity [Hz/cm^{2}]',
		'Comparator-Strip Efficiency',
		'lumi'
	)