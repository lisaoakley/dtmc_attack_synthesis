# 20 params
for j in 0 1 2 3 4
do
for i in 5 10 15
do
    ./run --property "P=? [s!=${i} U s=$((${i}*${i}-1))]" --method concrete   --epsilon .05 --tm_SPSS $((${i}+1)) $((${i}+2)) $((${i}+3)) $((2*${i}+1)) --case_study gridworld --id ${i}x${i}rand000${j} --property_tag scale_until
done
done