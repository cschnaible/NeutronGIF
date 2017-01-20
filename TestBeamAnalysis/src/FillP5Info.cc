#include "Gif/TestBeamAnalysis/interface/FillP5Info.h"

void FillP5EventInfo::fill(float sT_)
{
	reset();
	sT = sT_;
}

void FillP5MuonInfo::fill(const std::vector<reco::Muon> &muons)
{
	reset();
	muon_charge   = { muons[0].charge(), muons[1].charge() };
	muon_pT       = { muons[0].pt()    , muons[1].pt()     };
	muon_eta      = { muons[0].eta()   , muons[1].eta()    };
	muon_phi      = { muons[0].phi()   , muons[1].phi()    };
	muon_pZ       = { muons[0].pz()    , muons[1].pz()     };

	for (auto &muon : muons)
	{
		std::vector<unsigned short int> chambers;
		for (auto &match : muon.matches())
		{
			if (match.detector() != MuonSubdetId::CSC) continue;
			CSCDetId cscId(match.id);
			unsigned short int id = GIFHelper::chamberSerial(cscId);
			chambers.push_back(id);
		}
		muon_chamlist.push_back(chambers);
		chambers.clear();
	}
}

void FillP5ZInfo::fill(const std::vector<reco::Muon> &muons)
{
	reset();
	ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> Z = muons[0].p4() + muons[1].p4();
	Z_pT       = Z.pt()  ;
	Z_rapidity = Z.y()   ;
	Z_eta      = Z.eta() ;
	Z_phi      = Z.phi() ;
	Z_pZ       = Z.pz()  ;
	Z_mass     = Z.mass();
}
