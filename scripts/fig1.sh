
# SPSS eps=.1
./run --property "P=? [(s!=2) U<=10 s=3 ]" --property_tag 'until10_fig1' --method concrete   --epsilon .1 --tm_SPSS 1 --case_study fig1 --id fig1
# SPST eps=.1
./run --property "P=? [(s!=2) U<=10 s=3 ]" --property_tag 'until10_fig1' --method concrete   --epsilon .1 --tm_SPST 0,0 0,1 0,2 1,0 1,1 1,2 2,0 2,1 2,2 --case_study fig1 --id fig1

# SS eps=.1
./run --property "P=? [(s!=2) U<=10 s=3 ]" --property_tag 'until10_fig1' --method concrete   --epsilon .1 --tm_SS 1 --case_study fig1 --id fig1
# ST eps=.1
./run --property "P=? [(s!=2) U<=10 s=3 ]" --property_tag 'until10_fig1' --method concrete   --epsilon .1 --tm_ST 0,0 0,1 0,2 1,0 1,1 1,2 2,0 2,1 2,2 --case_study fig1 --id fig1