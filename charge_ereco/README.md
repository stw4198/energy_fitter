This fitter is designed to calculate the fits for energy reconstruction in neutrino detectors using the photoelectrons detected by the PMTs for each event.

Use MCextract to extract the information from the Monte Carlo simulation. Use efit to determine the energy fits and resolution. efit can be used on either the MCextract output root file or the reconstructed vertex output file from FRED.

To compile the fitters, use make [file name] (neglect '.cc').

To extract MC information, do ./MCextract [input].root [output].root [event\_information].csv [pmt\_hit\_information].csv

To calculate energy fits, do ./efit [input].root

The input for efit should be the output of FRED or MCextract
