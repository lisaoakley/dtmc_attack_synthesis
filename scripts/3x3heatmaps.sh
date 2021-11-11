# SPSS eps=.1
./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6' --method concrete   --epsilon .1 --tm_SPSS 1 3 7 --case_study gridworld --id 3x3heatmaps
# SPSS eps=.2
./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6' --method concrete   --epsilon .3 --tm_SPSS 1 3 7 --case_study gridworld --id 3x3heatmaps

# SS eps=.1
./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6' --method concrete   --epsilon .1 --tm_SS 1 3 7 --case_study gridworld --id 3x3heatmaps
# SS eps=.2
./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6' --method concrete   --epsilon .3 --tm_SS 1 3 7 --case_study gridworld --id 3x3heatmaps