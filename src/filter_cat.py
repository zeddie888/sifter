# Example script to produce a filtered star catalog from YBSC

from parse_bsc import *

write_filtered_catalog("bsc.tsv", "foo.csv", 6, 0.05)