#!/bin/sh


trans1="2,2 2,3 2,7 2,8 3,2 3,3 3,7 3,8 3,9 3,4 4,3 4,4 4,8 4,9 7,2 7,3 7,7 7,8 8,2 8,3 8,4 8,7 8,8 8,9 9,4 9,3 9,8 9,9"
trans2="2,2 2,3 2,7 2,8 3,2 3,3 3,7 3,8 3,9 3,4 4,3 4,4 4,8 4,9 7,2 7,3 7,7 7,8 7,12 7,13 8,2 8,3 8,4 8,7 8,8 8,9 8,12 8,13 8,14 9,4 9,3 9,8 9,9 9,13 9,14 12,7 12,8 12,12 12,13 13,7 13,8 13,9 13,12 13,13 13,14 14,8 14,9 14,13 14,14"

# Multiple GWs
for j in 0
do
# Multiple epsilons
for eps in 0.05 0.1 0.15 0.2 0.25 0.3
do

# SPST trans1
./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SPST ${trans1} --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# ST trans2
./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_ST ${trans1} --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# SPST trans1
./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SPST ${trans2} --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# ST trans2
./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_ST ${trans2} --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"


# # SPSS 3 states
# ./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SS 1 3 10 --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# # SS 3 states
# ./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SPSS 1 3 10 --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# # SPSS 5 states
# ./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SS 1 3 10 12 19 --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

# # SS 5 states
# ./run --property "P=? [F<=200 s=24]" --method concrete   --epsilon ${eps} --tm_SPSS 1 3 10 12 19 --case_study gridworld --id 5x5rand000${j} --property_tag "eventually200"

done
done

