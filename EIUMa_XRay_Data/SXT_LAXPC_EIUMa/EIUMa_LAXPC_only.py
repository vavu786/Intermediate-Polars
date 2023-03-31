# To run this script, type 
# ~$ sherpa filename.py

# Load files
load_pha(1, "lxp2level2.spec")
load_pha(2, "lxp2level2back_shifted.spec")
load_rmf(1, "lx20cshm06L1v1.0.rmf")
load_rmf(2, "lx20cshm06L1v1.0.rmf")

# Background
set_source(2, powlaw1d.p1 + powlaw1d.p2)

# Source
set_source(1, (xstbabs.abs1) * (xscevmkl.c1 + p1 + p2))

# Systematic errors
set_syserror(1, 0.03, fractional=True)
set_syserror(2, 0.03, fractional=True)

# Change of domains
notice_id([1, 2], 3.0, 20.0)

# Freezing column density value
abs1.nH.val = 0.033
abs1.nH.freeze()

# Fitting backgrounds first, then fold over to the sources

# Values from SXT+LAXPC combined fit that produced a good LAXPC bkg fit
p1.gamma = -0.78
p1.ref = 1
p1.ampl = 3.58e-05

p2.gamma = 2.17
p2.ref = 1
p2.ampl = 0.0296

fit(2)
freeze(p1, p2)

# Re-fit

#guess(c1)
#guess(abs2)

#c1.kT = 52
#c1.kT.freeze()
#abs2.nH = 1.7


fit()
plot("fit", 1, "fit", 2)

#for i in range(1, 5):
#	plot("fit", i)
#	plt.savefig("

