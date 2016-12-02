import numpy as np
import ROOT as R
import Gif.TestBeamAnalysis.Primitives as Primitives
import DisplayHelper as ED # "Event Display"

##########
# This file gets the data, makes the histograms, makes the objects, and makes the plots
# It is the true meat of the analysis; anything cosmetic or not directly relevant should
# be moved to one of the other files: Primitives for classes, DisplayHelper for cosmetics
##########

R.gROOT.SetBatch(True)

##### PARAMETERS #####
# Measurement List, Chamber IDs (1, 110), Event List (1 indexed)
MEASLIST = [3284, 3384]
CHAMS    = [1, 110]
EVENTS   = [1, 2, 3, 4, 5]

# ADC Time Bin (1 indexed), RecHit Strip List (1 indexed; must be improper subset of [1, 2, 3])
TIMEBIN      = 3
RECHITSTRIPS = [2]

# Which displays to plot
DODISPLAYS = True
DORECHITS  = True

##### BEGIN CODE #####
for MEAS in MEASLIST:
	# Get file and tree
	f = R.TFile.Open('/afs/cern.ch/work/c/cschnaib/public/GIF/test/ana_'+str(MEAS)+'.root')
	t = f.Get('GIFTree/GIFDigiTree')

	for EVENT in EVENTS:
		# Get the event, make the ETree, and make lists of primitives objects
		t.GetEntry(EVENT-1)
		E = Primitives.ETree(t) # default DecList
		wires   = [Primitives.Wire  (E, i) for i in range(len(E.wire_cham ))]
		strips  = [Primitives.Strip (E, i) for i in range(len(E.strip_cham))]
		comps   = [Primitives.Comp  (E, i) for i in range(len(E.comp_cham ))]
		rechits = [Primitives.RecHit(E, i) for i in range(len(E.rh_cham   ))]

		for CHAM in CHAMS:
			# Upper limits for wire group numbers and half strip numbers
			WIRE_MAX = 50   if CHAM == 1 else 113
			HS_MAX   = 230  if CHAM == 1 else 164

			if DODISPLAYS:
				##### PRIMITIVES DISPLAY #####

				# Instantiate canvas
				canvas = ED.Canvas('primitives')

				# Calculate pedestal
				try:
					PEDESTAL = min([min([i for i in strip.ADC]) for strip in strips if strip.cham == CHAM])
				except:
					PEDESTAL = 0

				# Wires histogram: 2D, wire group vs. layer, weighted by time bin
				hWires = R.TH2F('wires', 'ANODE HIT TIMING;Wire Group Number;Layer;Timing', WIRE_MAX, 0, WIRE_MAX, 6, 1, 7)
				hWires.GetZaxis().SetRangeUser(0,16)
				for wire in wires:
					if wire.cham != CHAM: continue
					hWires.Fill(wire.number, wire.layer, wire.timeBin)
				canvas.pads[2].cd()
				hWires.Draw('colz')

				# Comparators histogram: 2D, staggered half strip vs. layer, weighted by time bin
				hComps = R.TH2F('comps', 'COMPARATOR HIT TIMING;Half Strip Number;Layer;Timing', HS_MAX, 0, HS_MAX, 6, 1, 7)
				hComps.GetZaxis().SetRangeUser(0,16)
				for comp in comps:
					if comp.cham != CHAM: continue
					hComps.Fill(comp.staggeredHalfStrip, comp.layer, comp.timeBin)
				canvas.pads[1].cd()
				hComps.Draw('colz')

				# ADC Count histogram: 2D, staggered strip vs. layer, weighted by ADC count minus pedestal (smallest ADC count for this measurement)
				hADC = R.TH2F('adc', 'CATHODE STRIP ADC COUNT, BIN '+str(TIMEBIN+1)+';Strip Number;Layer;ADC #minus '+str(PEDESTAL), HS_MAX, 0, HS_MAX/2, 6, 1, 7)
				for strip in strips:
					if strip.cham != CHAM: continue
					hADC.Fill(strip.staggeredNumber      , strip.layer, strip.ADC[TIMEBIN]-PEDESTAL)
					hADC.Fill(strip.staggeredNumber + 0.5, strip.layer, strip.ADC[TIMEBIN]-PEDESTAL)
				canvas.pads[0].cd()
				hADC.Draw('colz')

				# lumi text: m#MEAS, MEX/1, Event # EVENT
				canvas.drawLumiText('m#'+str(MEAS)+', ME'+('1' if CHAM == 1 else '2')+'/1, Event #'+str(EVENT))

				# save as: ED_MEAS_MEX1_EVENT.pdf
				canvas.canvas.SaveAs('pdfs/ED_'+str(MEAS)+'_ME'+('1' if CHAM == 1 else '2')+'1_'+str(EVENT)+'.pdf')
				print '\033[1mFILE \033[32m'+'EH_'+str(MEAS)+'_ME'+('1' if CHAM == 1 else '2')+'1_'+str(EVENT)+'.pdf'+'\033[30m CREATED\033[0m'

			if DORECHITS:
				##### RECHITS DISPLAY #####

				# Instantiate canvas
				canvas = ED.Canvas('rechits')

				# Wires histogram: 2D, wire group vs. layer, weighted by time bin
				hRHWG = R.TH2F('rhwg', 'RECHIT WIRE GROUPS;Wire Group Number;Layer;Multiplicity', WIRE_MAX, 0, WIRE_MAX, 6, 1, 7)
				#hRHWG.GetZaxis().SetRangeUser(0,16)
				for rh in rechits:
					if rh.cham != CHAM: continue
					hRHWG.Fill(rh.wireGroup, rh.layer, 1)
				canvas.pads[1].cd()
				hRHWG.Draw('colz')

				# Strips histogram: 2D, 3 strips vs. layer, weighted by time bin
				addOn = ', STRIP'
				if len(RECHITSTRIPS) == 1:
					addOn += ' ' + str(RECHITSTRIPS[0])
				else:
					addOn += 'S '
					for i,STRIP in enumerate(RECHITSTRIPS):
						addOn += str(STRIP) + (', ' if i<len(RECHITSTRIPS)-1 else '')
				hRHS = R.TH2F('rhs', 'RECHIT STRIPS'+addOn+';Strip Number;Layer;Multiplicity', HS_MAX/2, 0, HS_MAX/2, 6, 1, 7)
				#hRHS.GetZaxis().SetRangeUser(0,16)
				for rh in rechits:
					if rh.cham != CHAM: continue
					for STRIP in RECHITSTRIPS:
						hRHS.Fill(rh.strips[STRIP-1], rh.layer, 1)
				canvas.pads[0].cd()
				hRHS.Draw('colz')

				# lumi text: m#MEAS, MEX/1, Event # EVENT
				canvas.drawLumiText('m#'+str(MEAS)+', ME'+('1' if CHAM == 1 else '2')+'/1, Event #'+str(EVENT))

				# save as: RD_MEAS_MEX1_EVENT.pdf
				canvas.canvas.SaveAs('pdfs/RH_'+str(MEAS)+'_ME'+('1' if CHAM == 1 else '2')+'1_'+str(EVENT)+'.pdf')
				print '\033[1mFILE \033[32m'+'RH_'+str(MEAS)+'_ME'+('1' if CHAM == 1 else '2')+'1_'+str(EVENT)+'.pdf'+'\033[30m CREATED\033[0m'

	f.Close()
