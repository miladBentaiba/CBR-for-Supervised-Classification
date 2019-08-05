import init
from constants import SOLUTION, POSSIBLE_SOLUTIONS

S = init.Singleton.get_instance()
_c = S.cursor()
_c.execute('select * from main.test_cases')
test_cases = []
for row in _c.fetchall():
    test_cases.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))

statistics = {}
for x1 in POSSIBLE_SOLUTIONS:
    statistics[str(x1)+str(x1)] = 0
    statistics[str(x1) + "x"] = 0
# --------------------------------------------------------------------------------------------------------
# I_NS_CB with similarity 0.8
_c.execute('select * from main.cases where stochasticity >= 0.8')
cases = []
for row in _c.fetchall():
    cases.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))


from cases_similarity import compare_cases_initial

for test_case in test_cases:
    found = None
    original_solution = test_case[SOLUTION]
    for case in cases:
        # verification per similarity
        if compare_cases_initial(case, test_case) > 0.8:
            if case[SOLUTION] == test_case[SOLUTION]:
                found = True
                break
        # verification per rules
        from absolute_validation import validation_per_rules
        if found == None:
            for solution in POSSIBLE_SOLUTIONS:
                test_case[SOLUTION] = solution
                if validation_per_rules(test_case):
                    if solution == original_solution:
                        found = True
                        break
                    else:
                        found = False
                        break
                elif not validation_per_rules(test_case):
                    if solution == original_solution:
                        found = False
                        break
    if found == True:
        statistics[str(original_solution)+str(original_solution)] += 1
    elif found == False:
        statistics[str(original_solution)+"x"] += 1
    else:
        print("found is none", found == None)
        statistics[str(original_solution) + str(original_solution)] += 1

print(statistics)
