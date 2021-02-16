This fitter is designed to calculate the fits for energy reconstruction in neutrino detectors using the photoelectrons detected by the PMTs for each event.

Use efit to extract the information from the Monte Carlo simulation. Use pe\_E to determine the energy fits and resolution. pe\_E can be used on either the efit output root file or the reconstructed vertex output file from FRED.

To compile the fitters, use make [file name] (neglect '.cc').

To extract MC information, do ./efit [input].root [output].root [event\_information].csv [pmt\_hit\_information].csv

To calculate energy fits, do ./pe\_E [input].root

The input for pe\_E should be the output of FRED or efit
