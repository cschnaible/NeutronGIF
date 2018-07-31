# Bob neutron play starting from bob_binomial.C
# Rewritten in python by Chris
# Takes two command line arguments : m (nuclear mass in MeV) T (temp in Kelvin)
# Outputs a pdf of the Maxwell Boltzmann distribution
# Example useage : 
# $ python thermal.py 939. 290.
   
import ROOT as R
import numpy as np
import sys as sys

def KEtest(m, T):
	'''
	m is nuclear mass in MeV, T is temp in Kelvin
	Answer for KE should not depend on mass! Intermediate v's do.
	'''

	KEhist = R.TH1F("KEhist", "Maxwell-Boltzmann;Energy [eV];Counts", 300, 0.0, 0.3)

	# scale T to MeV
	kT = 0.025*(10**-6)*T/290.1  #kT in MeV
	mean = 0.
	sigma = np.sqrt(kT/m); #sigma of Gaussian for component of 3-vector velocity

	for j in range(1000000):

		# 3-vector velocity
		v = np.random.normal(mean,sigma,3)
		print 'm %s T %s sigma %s v %s' % (m,T,sigma,v)
		p = m * v
		vsq = sum(v**2)
		kin = 0.5*m*vsq;

		# cross check
		psq = sum(p**2)

		#print 'kin %s %s %s'%(kin, psq/(2*m), kin*10**6)

		KEhist.Fill(kin*10**6);

	c1= R.TCanvas("c1", "random",5,5,800,600);
	c1.SetTicks(1,1);

	KEhist.Draw();
	c1.SaveAs('MaxwellBoltzmann.pdf')

if __name__=='__main__':
	m = sys.argv[1]
	T = sys.argv[2]
	KEtest(float(m),float(T))
