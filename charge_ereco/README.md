This fitter is designed to calculate the fits for energy reconstruction in neutrino detectors using the photoelectrons detected by the PMTs for each event.

Use MCextract to extract the information from the [RAT-PAC](https://github.com/AIT-WATCHMAN/rat-pac.git) Monte Carlo simulation. Use efit to determine the energy fits and resolution. efit can be used on either the MCextract output root file or the reconstructed vertex output file from [FRED](https://github.com/AIT-WATCHMAN/FRED.git).

To compile the fitters, use make {file name} (neglect '.cc).

To extract MC information, do ./MCextract {input}.root {output}.root {event information}.csv {pmt hit information}.csv

To calculate energy fits, do ./efit {input}.root {fit parameter file} {resolution file} {plot name}

The input for efit should be the output of FRED or MCextract
