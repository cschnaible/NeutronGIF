# Test Beam Analysis

## Documentation

## To-Do List -- August 8, 2016
  - [ ] __RIJU:__ Incorporate meta into TestBeamMeasurements.py
    * Only if .root file exists
  - [ ] __CHRIS:__ Figure out an equivalent of the dPhi penalty at GIF++ using the information in the CSCSegment class
    * [MuonCSCSeedFromRecHits.cc](https://github.com/cms-sw/cmssw/blob/CMSSW_7_5_X/RecoMuon/MuonSeedGenerator/src/MuonCSCSeedFromRecHits.cc)
    * Make additional option for with homebrew angle cut
  - [ ] __RIJU:__ Make segment quality histograms
    * [Note]: normalize to integral to start with; eventually normalize to scintillator scalar or something
    * nEvents vs. highest segment quality (i.e. lowest `segment_quality`) of all segments in event 
      - frequency distribution of "event best segments"
      - plot all the attenuations on top of each other
    * nEvents vs. quality of -all- segments
  - [ ] __CHRIS:__ Make segment nHits histogram
    * nHits, normalized to an nHits reference bin (i.e. 4 histograms, 4 bins each for 3, 4, 5, 6 hits)
  - [ ] __CHRIS:__ Make control plots of all quantities that contribute to the	`segmentQuality` function

### On Deck
  - [ ] Make efficiency plots for segment quality cuts
  - [ ] Talk about P5 plans
    * Getting the number of neutron hits per station

## To-Do List -- August 4, 2016

### For Riju
  - [x] Make timestamp plots but with orbit number and bunch crossing number
    * No orbit number or bunch crossing number saved in unpacked ROOT files -- probably not in RAW
    * The timestamps were found to be the timestamps at time of unpacking, so no beam structure recorded
  - [x] Implement Segment Quality function from RecoMuon/MuonSeedGenerator/src/MuonCSCSeedFromRecHits.cc
  - [x] Implement setStyle function
    * Added full Plotter classes
  - [x] Incorporate any stray scripts into TestBeamAnalysis
    * Added database and current scrapers and whatever analysis scripts I had

### For Chris
  - [x] Make plots of normalized segment nHits vs. attenuation (MOVED UPWARDS)
  - [x] Write script for dumping event content information, initially for empty segments
    * Histograms of nSegments and nLCTs vs presence or no presence of the other -- why?