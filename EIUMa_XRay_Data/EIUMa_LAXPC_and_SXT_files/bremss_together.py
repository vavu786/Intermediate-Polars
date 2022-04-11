# To run this script, type 
# ~$ sherpa excellent_fit.py

# Load files
load_pha(1, "EIUma_spectrum.pha")
load_bkg(1, "SkyBkg_comb_EL3p5_Cl_Rd16p0_v01.fits")
load_arf(1, "sxt_pc_excl00_v04_20190608.arf")
load_rmf(1, "sxt_pc_mat_g0to12.rmf")
load_bkg_arf(1, "sxt_pc_excl00_v04_20190608.arf")
load_bkg_rmf(1, "sxt_pc_mat_g0to12.rmf")

load_pha(2, "lxp2level2.spec")
load_bkg(2, "lxp2level2back_shifted.spec")
load_rmf(2, "lx20cshm06L1v1.0.rmf")
load_bkg_rmf(2, "lx20cshm06L1v1.0.rmf")


# First gaussian: compensates for the large spike at around 0.38 keV
create_model_component("xsgaussian", "bkgg1")
bkgg1.LineE = 0.38
bkgg1.Sigma = 0.009
bkgg1.norm = 0.0011
bkgg1.LineE.freeze()
bkgg1.Sigma.freeze()
bkgg1.norm.freeze()

# Second gaussian: compensates for a dip around 0.58 keV
create_model_component("xsgaussian", "bkgg2")
bkgg2.LineE = 0.58
bkgg2.norm = 0.011
bkgg2.LineE.freeze()

# Third gaussian: compensates for a dip around 0.88 keV
create_model_component("xsgaussian", "bkgg3")
bkgg3.LineE = 0.88
bkgg3.norm = 0.011
bkgg3.LineE.freeze()

# Source models
set_source(1, (xstbabs.abs1 + xstbabs.abs2) * (xsbremss.c1 + powlaw1d.p1 + powlaw1d.p2))
set_bkg_model(1, powlaw1d.bkgp1 + powlaw1d.bkgp2 + bkgg1 + bkgg2 + bkgg3)
set_source(2, (xstbabs.abs3 + xstbabs.abs4) * (xsbremss.c2 + xsgaussian.g2 + powlaw1d.p3 + powlaw1d.p4))# + p5))
set_bkg_model(2, powlaw1d.bkgp3 + powlaw1d.bkgp4)

# Link Parameters
#bkgp1.gamma = p1.gamma
#bkgp2.gamma = p2.gamma

#bkgp3.gamma = p3.gamma
#bkgp4.gamma = p4.gamma

# Systematic errors
set_syserror(1, 0.02, fractional=True)
set_syserror(2, 0.03, fractional=True)

# Change of domains
notice_id(1, 0.31, 5)
notice_id(2, 3.0, 20.0)

# Freezing column density value
abs1.nH.val = 0.033
abs1.nH.freeze()

# Fitting backgrounds first, then fold over to the sources
fit_bkg(1, 2)
#plot_bkg_fit_delchi(1, 2)
#input("Press enter to continue: ")
freeze(bkgp1, bkgp2, bkgg1, bkgg2, bkgg3, bkgp3, bkgp4)

fit(1, 2)
plot_fit(1, 2)
input("Press enter to continue: ")
plot_bkg_fit(1, 2)

