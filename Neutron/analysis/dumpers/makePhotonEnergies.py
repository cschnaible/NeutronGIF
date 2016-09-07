import sys
from Gif.Neutron.Particle import Unpickle
from Gif.Neutron.Tools import eprint

# New after addition of daughter class: important name changes whenever daughters are mentioned

# Requires 1 argument, the suffix used when making the tree
if len(sys.argv) < 2:
	eprint('Usage: script.py SUFFIX')
	exit()

parts = Unpickle(sys.argv[1])

eprint('Starting analysis.')

# fill lists of IDs of neutrons, end neutrons, and captured
neutrons = [parts[p].ID for p in parts.keys() if parts[p].name == 'neutron']
endneutrons = []
captured = []

for nID in neutrons:
	foundN = False
	for d in parts[nID].daughters:
		if d.name == 'neutron':
			foundN = True
			break
	if not foundN:
		endneutrons.append(nID)
		if parts[nID].process == 'nCapture':
			captured.append(nID)

eprint("%i neutrons; %i end neutrons; %i captured neutrons" % (len(neutrons), len(endneutrons), len(captured)))

# for cutting on some threshold distance thresh in cm
def isWithin(r1, r2, thresh=0.1):
	return (sum([(i-j)**2 for i,j in zip(r1,r2)]))**0.5 < thresh

# make photon energy list
for nID in captured:
	print '%.4e' % parts[nID].energy_final,
	for d in parts[nID].daughters:
		if isWithin(parts[nID].pos_final, d.pos) and d.name == 'gamma':
			print '%.4e' % (d.energy),
	print ''
