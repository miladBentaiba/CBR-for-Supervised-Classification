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
    for x2 in POSSIBLE_SOLUTIONS:
        statistics[str(x1) + str(x2)] = 0


# --------------------------------------------------------------------------------------------------------
# I_NS_CB with similarity 0.8, add expert = true
# R_NS_CB with similarity 0.8
def NS_CB_Accuracy():
    cases = []
    _c.execute('select * from main.cases where stochasticity >= 0.9')
    for row in _c.fetchall():
        cases.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))

    from cases_similarity import compare_cases_initial
    for test_case in test_cases:
        found = None
        original_solution = test_case[SOLUTION]
        for case in cases:
            # verification per similarity
            if compare_cases_initial(case, test_case) > 0.9:
                if case[SOLUTION] == test_case[SOLUTION]:
                    found = True
                    statistics[str(original_solution) + str(original_solution)] += 1
                    break

            # verification per rules
            from absolute_validation import validation_per_rules
            if found is None:
                for solution in POSSIBLE_SOLUTIONS:
                    test_case[SOLUTION] = solution
                    rules = validation_per_rules(test_case)
                    if rules[0]:
                        found = False
                        statistics[str(original_solution) + str(rules[1])] += 1
                    elif not rules[0]:
                        if solution == original_solution:
                            statistics[str(original_solution) + str(rules[1])] += 1
                            found = False
            if found is None:
                for soll in POSSIBLE_SOLUTIONS:
                    statistics[str(original_solution) + str(soll)] += 1


    print(statistics)
    return statistics


# # ------------------------------------------------------------------------------------------------------
# # I_NS_CB with similarity 0.8, add expert = true
# # R_NS_CB with similarity 0.8
def S_CB_Accuracy():
    from segmentation import get_delegates_by_solution
    from case_segment_similarity import compare_case_delegate
    delegates= {}
    for solution in POSSIBLE_SOLUTIONS:
        delegates[solution] = get_delegates_by_solution(solution)
    # for each test_case
    for test_case in test_cases:
        found = None
        # delegates = get_delegates_by_solution(test_case[SOLUTION])
        for delegate in delegates[test_case[SOLUTION]]:
            similarity = compare_case_delegate(test_case, delegate['delegate'])
            if similarity > 0.9:
                found = True
                statistics[str(test_case[SOLUTION]) + str(test_case[SOLUTION])] += 1
                break
        if found is None:
            for solution in POSSIBLE_SOLUTIONS:
                if solution != test_case[SOLUTION]:
                    delegatess = get_delegates_by_solution(test_case[SOLUTION])
                    for delegate in delegatess:
                        similarity = compare_case_delegate(test_case, delegate['delegate'])
                        if similarity > 0.9:
                            found = False
                            statistics[str(test_case[SOLUTION]) + str(solution)] += 1
        if found is None:
            # verification per rules
            from absolute_validation import validation_per_rules
            if found is None:
                for solution in POSSIBLE_SOLUTIONS:
                    test_case[SOLUTION] = solution
                    rules = validation_per_rules(test_case)
                    if rules[0]:
                        found = False
                        statistics[str(test_case[SOLUTION]) + str(rules[1])] += 1
                    elif not rules[0]:
                        if solution == test_case[SOLUTION]:
                            statistics[str(test_case[SOLUTION]) + str(rules[1])] += 1
                            found = False
                            break
            if found is None:
                for soll in POSSIBLE_SOLUTIONS:
                    statistics[str(test_case[SOLUTION]) + str(soll)] += 1
    print(statistics)
    return statistics


print("I_NS_CB 10%")
NS_CB_Accuracy()
print("I_S_CB 10%")
S_CB_Accuracy()
