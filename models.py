def eSC(params, (n1,n2), pts):
	"""
	Secondary contact model with population change.
  	by E. Wong, modified from Tine et al. 2014.
	S: Size of pop 1 after split. (Pop 2 has size 1-s)
	N1: Size of population 1 after split.
	N2: Size of population 2 after split.
	M12: Migration from pop 2 to pop 1 (2*Na*M12).
	M21: Migration from pop 1 to pop 2.
	Ta: The scaled time between the split and the secondary contact (in units of 2*Na generations).
	Ts: The scale time between secondary contact and present.
	n1,n2: Size of fs to generate.
	pts: Number of points to use in grid for evaluation.
	"""
	S, N1, N2, M12, M21, Ta, Ts = params
	
	xx = dadi.Numerics.default_grid(pts)
	
	N1_func = lambda t: S * (N1/S)**(t/(Ta+Ts))
	N2_func = lambda t: (1-S) * (N2/(1-S))**(t/(Ta+Ts))

	phi = dadi.PhiManip.phi_1D(xx)
	phi = dadi.PhiManip.phi_1D_to_2D(xx, phi)
	phi = dadi.Integration.two_pops(phi, xx, Ta, N1_func, N2_func, M12=0, M21=0)
	phi = dadi.Integration.two_pops(phi, xx, Ts, N1_func, N2_func, M12=M12, M21=M21)
	
	fs = dadi.Spectrum.from_phi(phi, (n1,n2), (xx,xx))
	return fs


def IM_2M_AL_SC(params, ns, pts): 
	""" 
	Isolation-with-migration model with exponential pop growth and 2 classes of migration, 
 	period of allopatry followed by secondary contact, then 2 classes of migration.
	by E. Wong, modified from Nevado et al. 2018.
	S: Size of pop 1 after split. (Pop 2 has size 1-s.) 
	N1: Final size of pop 1. 
	N2: Final size of pop 2. 
	Ta: Duration of migration after split (in unites of 2*Na generations) 
	Ts: Duration of allopatric phase (in units of 2*Na generations)  
	Tm: Duration of secondary contact phase (in units of 2*Na generations)  
	Ma: Migration in site class 1 (2*Na*m12) in Ta
	Mb: Migration in site class 2 in Ta
	Mc: Migration in site class 1 (2*Na*m12) in Tm
	Md: Migration in site class 2 in Tm
	P: proportion of class 1 sites
	n1,n2: Sample sizes of resulting Spectrum 
	pts: Number of grid points to use in integration. 
	""" 
	S,N1,N2,Ta,Ts,Tm,Ma,Mb,Mc,Md,P = params 
	
	xx = dadi.Numerics.default_grid(pts) 

	N1_func = lambda t: S * (N1/S)**(t/(Ta+Ts+Tm)) 
	N2_func = lambda t: (1-S) * (N2/(1-S))**(t/(Ta+Ts+Tm)) 

	# site class 1
	phi = dadi.PhiManip.phi_1D(xx) 
	phi = dadi.PhiManip.phi_1D_to_2D(xx, phi) 
	phi = dadi.Integration.two_pops(phi, xx, Ta, N1_func, N2_func, M12=Ma, M21=Ma) 
	phi = dadi.Integration.two_pops(phi, xx, Ts, N1_func, N2_func, M12=0, M21=0) 
	phi = dadi.Integration.two_pops(phi, xx, Tm, N1_func, N2_func, M12=Mc, M21=Mc) 
	fs1 = dadi.Spectrum.from_phi(phi, ns, (xx,xx)) 
	
	# site class 2
	phi2 = dadi.PhiManip.phi_1D(xx) 
	phi2 = dadi.PhiManip.phi_1D_to_2D(xx, phi2) 
	phi2 = dadi.Integration.two_pops(phi, xx, Ta, N1_func, N2_func, M12=Mb, M21=Mb) 
	phi2 = dadi.Integration.two_pops(phi2, xx, Ts, N1_func, N2_func, M12=0, M21=0) 
	phi2 = dadi.Integration.two_pops(phi2, xx, Tm, N1_func, N2_func, M12=Md, M21=Md) 
	fs2 = dadi.Spectrum.from_phi(phi2, ns, (xx,xx)) 

	fs = P*fs1+(1-P)*fs2
	return fs 
