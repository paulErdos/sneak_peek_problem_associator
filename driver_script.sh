#!/usr/bin/bash

for sample_solution in sample_solutions/*;
    do
    sample_exam=$(echo $sample_solution | sed 's|sample_solutions\/\([^\.]\+\).txt|\1|');
    sample_exam="sample_exams/cmps112-"$sample_exam".tt"

    ls $sample_exam
    ls $sample_solution
    echo
    ./problem_finder.py wordlist.txt $sample_exam $sample_solution
done
