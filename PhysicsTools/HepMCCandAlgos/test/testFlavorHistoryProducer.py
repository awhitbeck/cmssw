# Import configurations
import FWCore.ParameterSet.Config as cms


process = cms.Process("testFlavorHistoryProducer")

        
# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)




# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# Load geometry
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('PHYS14_25_V2::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

# input MC stuff
process.load( "SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genParticles_cfi")
#process.load( "PhysicsTools.HepMCCandAlgos.genEventWeight_cfi")
#process.load( "PhysicsTools.HepMCCandAlgos.genEventScale_cfi")

process.load( "RecoJets.Configuration.GenJetParticles_cff")
#process.load( "RecoJets.JetProducers.SISConeJetParameters_cfi" )
process.load( "RecoJets.JetProducers.GenJetParameters_cfi" )
process.load( "RecoJets.JetProducers.FastjetParameters_cfi" )
#process.load( "RecoJets.JetProducers.sisCone5GenJets_cff")


# input flavor history stuff
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")
process.cFlavorHistoryProducer.src = cms.InputTag("prunedGenParticles")
process.cFlavorHistoryProducer.matchedSrc = cms.InputTag("slimmedGenJets")
process.bFlavorHistoryProducer.src = cms.InputTag("prunedGenParticles")
process.bFlavorHistoryProducer.matchedSrc = cms.InputTag("slimmedGenJets")
process.bFlavorHistoryProducer.verbose = True

process.printList = cms.EDAnalyzer( "ParticleListDrawer",
                                    src =  cms.InputTag( "prunedGenParticles" ),
                                    maxEventsToPrint = cms.untracked.int32( 10 )
#                                    printOnlyHardInteraction = cms.untracked.bool( True )
)




# request a summary at the end of the file
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# define the source, from reco input

process.source = cms.Source("PoolSource",
                        fileNames = cms.untracked.vstring(
        '/store/mc/Phys14DR/ZJetsToNuNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000D3972-D973-E411-B12E-001E67398142.root'
        )
                        )


# define event selection to be that which satisfies 'p'
process.eventSel = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)



# load the different paths to make the different HF selections


import PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi as flavortools


process.p         = cms.Path( flavortools.flavorHistorySeq * process.printList )


# Set the threshold for output logging to 'info'
process.MessageLogger.cerr.threshold = 'INFO'


# talk to output module


process.out = cms.OutputModule( "PoolOutputModule",
  process.eventSel,
  fileName = cms.untracked.string( "testFlavorHistoryProducer.root" ),
  outputCommands= cms.untracked.vstring(
    "drop *",
    "keep *_sisCone5GenJets_*_*",
    "keep *_genParticles_*_*",
#    "keep *_genEventWeight_*_*",
    "keep *_bFlavorHistoryProducer_*_*",
    "keep *_cFlavorHistoryProducer_*_*",
    "keep *_flavorHistoryFilter_*_*"
    )
                                )


# define output path
process.outpath = cms.EndPath(process.out)
