# To run this script, type 
# ~$ sherpa excellent_fit.py

# Load files
load_pha(1, "EIUma_spectrum.pha")
load_pha(2, "SkyBkg_comb_EL3p5_Cl_Rd16p0_v01.fits")
load_pha(3, "lxp2level2.spec")
load_pha(4, "lxp2level2back_shifted.spec")
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

# Gaussian for Fe line at 6.5 keV
create_model_component("xsgaussian", "laxpcbkgg1")
laxpcbkgg1.LineE = 7.0
laxpcbkgg1.LineE.freeze()

# Backgrounds
set_source(2, powlaw1d.p1 + powlaw1d.p2 + bkgg1 + bkgg2 + bkgg3)
set_source(4, powlaw1d.p3 + powlaw1d.p4)

# Source models
set_source(1, (xstbabs.abs1 + xstbabs.abs2) * (xsbremss.c1 + p1 + p2))
set_source(3, (xstbabs.abs3) * (xsbremss.c2 + laxpcbkgg1 + p3 + p4))

# XSPEC model cevmkl doesn't seem to work
#set_source(1, (xstbabs.abs1 + xstbabs.abs2) * (xscevmkl.c1 + p1 + p2))
#set_source(3, (xstbabs.abs3) * (xscevmkl.c2 + laxpcbkgg1 + p3 + p4))

laxpcbkgg1.LineE = 6.5
laxpcbkgg1.LineE.freeze()

# Systematic errors
set_syserror(1, 0.02, fractional=True)
set_syserror(2, 0.02, fractional=True)
set_syserror(3, 0.03, fractional=True)
set_syserror(4, 0.03, fractional=True)

# Change of domains
notice_id([1, 2], 0.31, 5) # previously 5.0
notice_id([3, 4], 3.0, 20.0)

# Freezing column density value
abs1.nH.val = 0.033
abs1.nH.freeze()

#guess(laxpcbkgg1)
# Fitting backgrounds first, then fold over to the sources
fit(2, 4)
freeze(p1, p2, bkgg1, bkgg2, bkgg3, p3, p4)

fit()
# Move the norm up a little to move it away from 0
#laxpcbkgg1.norm = 0.1

# Thaw the LineE for the LAXPC gaussian
#laxpcbkgg1.LineE.thaw()

# Re-fit
#fit()
#plot("fit", 1, "fit", 2, "fit", 3, "fit", 4)

# ___________________Confidence Countours_____________________ #

mkdir Code_Conf_Conts/

# No linking first
reg_proj(c1.kT, abs2.nH, min=[1.4, 1.5], max=[3.0, 4.5], nloop=[40, 40], sigma=[1, 1.6])
plt.savefig("Code_Conf_Conts/c1.kT_and_abs2.nH_nloop=40.png")

reg_proj(c1.kT, c2.kT, min=[1.4, 9.0], max=[3.0, 100], nloop=[40, 40], sigma=[1, 1.6])
plt.savefig("Code_Conf_Conts/c1.kT_and_c2.kT_nloop=40.png")

reg_proj(c2.kT, abs3.nH, nloop=[20, 20], sigma=[1, 1.6]) # keep at nloop=20
plt.savefig("Code_Conf_Conts/c2.kT_and_abs3.nH_nloop=20.png")

reg_proj(abs2.nH, abs3.nH, min=[1.4, 1.5], max=[3.0, 4.5], nloop=[20, 20], sigma=[1, 1.6]) # keep at nloop=20
plt.savefig("Code_Conf_Conts/abs2.nH_and_abs3.nH_nloop=20.png")

# Linked columns

link(abs3.nH, abs2.nH)
fit()

reg_proj(c2.kT, abs2.nH, min=[0.0, 1.0], max=[20.0, 4.5], nloop=[40, 40], sigma=[1, 1.6]) # testing rn
plt.savefig("Code_Conf_Conts/lc2.kT_and_abs2.nH_nloop=40.png")

reg_proj(c1.kT, abs2.nH, min=[1.0, 1.0], max=[3.0, 4.5], nloop=[40, 40], sigma=[1, 1.6])
plt.savefig("Code_Conf_Conts/lc1.kT_and_abs2.nH_nloop=40.png")

reg_proj(c1.kT, c2.kT, min=[1.0, 0.5], max=[3.0, 20.0], nloop=[40, 40], sigma=[1, 1.6])
plt.savefig("Code_Conf_Conts/lc1.kT_and_c2.kT_nloop=40.png")

#"/Images/Confidence\ Contours/Sigma_1_and_1.6/Non-linked\ columns/"
#"/Images/Confidence\ Contours/Sigma_1_and_1.6/Linked\ columns/"


