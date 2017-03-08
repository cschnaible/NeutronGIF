#ifndef FILLSIMINFO_H
#define FILLSIMINFO_H

#include "Gif/Production/interface/TreeContainer.h"

class FillSimHitInfo : public FillInfo
{
	public:
		FillSimHitInfo(TreeContainer &tree) : FillInfo(tree)
		{
			book("sim_id",sim_id);
			book("sim_particle_id",sim_particle_id);
			book("sim_process_type",sim_process_type);
			book("sim_lay",sim_lay);
			book("sim_pos_x",sim_pos_x);
			book("sim_pos_y",sim_pos_y);
			book("sim_pos_z",sim_pos_z);
			book("sim_pos_glb_x",sim_pos_glb_x);
			book("sim_pos_glb_y",sim_pos_glb_y);
			book("sim_pos_glb_z",sim_pos_glb_z);
			book("sim_tof",sim_tof);
			book("sim_energyLoss",sim_energyLoss);
			book("sim_entry_x",sim_entry_x);
			book("sim_entry_y",sim_entry_y);
			book("sim_entry_z",sim_entry_z);
			book("sim_exit_x",sim_exit_x);
			book("sim_exit_y",sim_exit_y);
			book("sim_exit_z",sim_exit_z);
			book("sim_pos_strip",sim_pos_strip);
			book("sim_pos_wire",sim_pos_wire);
			book("sim_entry_pabs",sim_entry_pabs);
			book("sim_entry_px",sim_entry_px);
			book("sim_entry_py",sim_entry_py);
			book("sim_entry_pz",sim_entry_pz);
		}
		virtual ~FillSimHitInfo() {};
		void fill(const CSCGeometry * theCSC, const edm::PSimHitContainer& simHits);

	private:
		std::vector<size16> sim_id;
		std::vector<int> sim_particle_id;
		std::vector<unsigned short> sim_process_type;
		std::vector<size8> sim_lay;
		std::vector<float> sim_pos_x;
		std::vector<float> sim_pos_y;
		std::vector<float> sim_pos_z;
		std::vector<float> sim_pos_glb_x;
		std::vector<float> sim_pos_glb_y;
		std::vector<float> sim_pos_glb_z;
		std::vector<float> sim_tof;
		std::vector<float> sim_energyLoss;
		std::vector<float> sim_entry_x;
		std::vector<float> sim_entry_y;
		std::vector<float> sim_entry_z;
		std::vector<float> sim_exit_x;
		std::vector<float> sim_exit_y;
		std::vector<float> sim_exit_z;
		std::vector<float> sim_pos_strip;
		std::vector<float> sim_pos_wire;
		std::vector<float> sim_entry_pabs;
		std::vector<float> sim_entry_px;
		std::vector<float> sim_entry_py;
		std::vector<float> sim_entry_pz;

		virtual void reset()
		{
			sim_id.clear();
			sim_particle_id.clear();
			sim_process_type.clear();
			sim_lay.clear();
			sim_pos_x.clear();
			sim_pos_y.clear();
			sim_pos_z.clear();
			sim_pos_glb_x.clear();
			sim_pos_glb_y.clear();
			sim_pos_glb_z.clear();
			sim_tof.clear();
			sim_energyLoss.clear();
			sim_entry_x.clear();
			sim_entry_y.clear();
			sim_entry_z.clear();
			sim_exit_x.clear();
			sim_exit_y.clear();
			sim_exit_z.clear();
			sim_pos_strip.clear();
			sim_pos_wire.clear();
			sim_entry_pabs.clear();
			sim_entry_px.clear();
			sim_entry_py.clear();
			sim_entry_pz.clear();
		}
};


#endif