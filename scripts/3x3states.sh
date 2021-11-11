
for i in 0 1 2 3 4 5 6 7 8
do
    # SPSS eps=.1
    ./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6_states' --method concrete   --epsilon .1 --tm_SPSS ${i} --case_study gridworld --id 3x3heatmaps
    # SPSS eps=.2
    ./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6_states' --method concrete   --epsilon .2 --tm_SPSS ${i} --case_study gridworld --id 3x3heatmaps

    # SS eps=.1
    ./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6_states' --method concrete   --epsilon .1 --tm_SS ${i} --case_study gridworld --id 3x3heatmaps
    # SS eps=.2
    ./run --property "P=? [(s!=2 & s!=6) U<=6 s=8 ]" --property_tag 'until6_states' --method concrete   --epsilon .2 --tm_SS ${i} --case_study gridworld --id 3x3heatmaps
done