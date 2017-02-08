import FWCore.ParameterSet.Config as cms
from Gif.Production.GIFTestBeamAnalysis_cfg import process

process.source = cms.Source('PoolSource', 
    fileNames = cms.untracked.vstring( 
        'file:doesnotexist.root',  
    ) 
)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('LogicError','ProductNotFound')
)
process.maxEvents.input = -1
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.p = cms.Path(process.muonCSCDigis * process.csc2DRecHits * process.cscSegments)

"""Customise digi/reco geometry to use unganged ME1/a channels"""
process.CSCGeometryESModule.useGangedStripsInME1a = False
process.idealForDigiCSCGeometry.useGangedStripsInME1a = False

process.GIFTree = cms.EDAnalyzer('MakeSimpleGIFTree',
						wireDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCWireDigi'),
						stripDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCStripDigi'),
						alctDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCALCTDigi'),
						clctDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCCLCTDigi'),
						lctDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCCorrelatedLCTDigi'),
						compDigiTag = cms.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi'),
						segmentTag = cms.InputTag('cscSegments'),
						recHitTag = cms.InputTag('csc2DRecHits'),
)
process.p *= process.GIFTree

