Two forms of energy fitting for use in neutrino detectors. Each folder has it's own README with instructions for use.

python_efit contains a pythonic fitter designed for use on events reconstructed in the WATCHMAN vertex fitter [FRED](https://github.com/AIT-WATCHMAN/FRED.git). It is designed to be adjustable by the user, but is not fast or highly organised. The fittig can be done using either photoelectrons desposited on PMTs or the number of PMTs hit in a given time window.

charge_ereco contains a C++ compilable fitter that uses the deposited photoelectrons on the PMT to fit energy. The fitter is designed to be used with either Monte Carlo events from [RAT-PAC](https://github.com/AIT-WATCHMAN/rat-pac.git) or with reconstructed events from FRED. If MC events are used, a value extractor is also provided to find all event and PMT hit values. This fitter is much faster as the reconstruction can be skipped.
