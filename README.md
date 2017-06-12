# sneak_peek_problem_associator
Professor Mackey at UCSC gives as a study guide for any upcoming exam two things:
1. Old exams
2. The upcoming exam, alphabetized, with duplicate words removed.
   He calls this a "sneak peek".

problem_finder.py takes old exams and the current sneak peek and checks how much
each problem matches the sneak peek. It then sorts the problems by the closeness
of the match into files, each file corresponding to a percentile. Additionally,
for each problem, the solution is copied into a corresponding file.

