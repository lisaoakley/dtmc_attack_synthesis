#!/bin/sh

# Multiple epsilons
for eps in 0.05 0.1 0.15 0.2 0.25 0.3  0.35 0.4 0.45 0.5
do
./run --property "P=? [F<=10 s=3]" --method concrete   --epsilon ${eps} --tm_SPSS 1 --case_study protocol --id protocol --property_tag "eventually10"
done

