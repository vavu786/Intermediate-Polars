# To run this script, type 
# ~$ sherpa script_name.py

# Load files
load_pha(1, "IGR16547_SXT_spectrum.pha")
load_pha(2, "SkyBkg_comb_EL3p5_Cl_Rd16p0_v01.fits")
load_pha(3, "lxp2level2.spec")
load_pha(4, "lxp2level2back.spec")
load_arf(1, "sxt_pc_excl00_v04_20190608.arf")
load_arf(2, "sxt_pc_excl00_v04_20190608.arf")
load_rmf(1, "sxt_pc_mat_g0to12.rmf")
load_rmf(2, "sxt_pc_mat_g0to12.rmf")
load_rmf(3, "lx20cshm06L1v1.0.rmf")
load_rmf(4, "lx20cshm06L1v1.0.rmf")

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

# Models
set_source(1, (xsconstant.c1 * xstbabs.abs1 * xspcfabs.pabs1) * ())
set_source(2, powlaw1d.p1 + powlaw1d.p2 + bkgg1 + bkgg2 + bkgg3)
set_source(3, (xstbabs.abs3 + xstbabs.abs4) * (xsbremss.c2 + xsgaussian.g2 + powlaw1d.plax))
set_source(4, powlaw1d.p3 + powlaw1d.p4)

# Systematic errors
set_syserror(1, 0.02, fractional=True)
set_syserror(2, 0.02, fractional=True)
set_syserror(3, 0.03, fractional=True)
set_syserror(4, 0.03, fractional=True)

# Change of domains
notice_id([1, 2], 0.31, 7.1)
notice_id([3, 4], 3.0, 20.0)

# Freezing column density value
abs1.nH.val = 0.123
abs1.nH.freeze()

# Fix gaussian at 6.5
# g1.LineE.val = 6.5
# g1.Sigma.val = 0.0
# g1.LineE.freeze()

# Fitting backgrounds first, then fold over to the sources
fit(2, 4)
plot("fit", 2, "fit", 4, xlog=True)
input("Press enter to continue: ")
freeze(p1, p2, p3, p4, bkgg1, bkgg2, bkgg3)

# Fitting each of them individually first, so they don't get stuck in local minima
#fit(1)
#fit(3)

fit(1, 2, 3, 4)
'''
counts_data = get_dep(1)
set_filter(1, counts_data > 0)

fit(1, 2, 3, 4)
'''
plot("fit", 1, "fit", 2, "fit", 3, "fit", 4)

