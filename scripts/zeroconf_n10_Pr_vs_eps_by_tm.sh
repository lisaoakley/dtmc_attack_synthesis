#!/bin/sh

# Multiple epsilons
for eps in 0.05 0.1 0.15 0.2 0.25 0.3
do

# SPSS first 5
./run --property "P=? [F<=30 s=13]" --method concrete   --epsilon ${eps} --tm_SPSS 1 2 3 4 5 --case_study zeroconf --id zeroconf_n10 --property_tag "eventually30"

# SPSS last 5
./run --property "P=? [F<=30 s=13]" --method concrete   --epsilon ${eps} --tm_SPSS 6 7 8 9 10 --case_study zeroconf --id zeroconf_n10 --property_tag "eventually30"


# SPSS 10
./run --property "P=? [F<=30 s=13]" --method concrete   --epsilon ${eps} --tm_SPSS 1 2 3 4 5 6 7 8 9 10 --case_study zeroconf --id zeroconf_n10 --property_tag "eventually30"


done

