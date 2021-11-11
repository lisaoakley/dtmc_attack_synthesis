for j in 0 1 2 3 4
do
for i in 5 10 20
do
    ./run --property "P=? [s!=${i} U s=$((${i}*${i}-1))]" --method symbolic   --epsilon .05 --tm_SPSS $((${i}+1)) --case_study gridworld --id ${i}x${i}rand000${j} --property_tag scale_until --pdtmc_modelchecker param --param_bin "/home/loakley/param/param-2-3-64"
done
done
