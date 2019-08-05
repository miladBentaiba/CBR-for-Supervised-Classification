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
        statistics[str(x1)+str(x2)] = 0


# --------------------------------------------------------------------------------------------------------
# I_NS_CB with similarity 0.8, add expert = true
# R_NS_CB with similarity 0.8
def NS_CB_Accuracy(initial):
    cases = []
    if initial is True:
        _c.execute('select * from main.cases where stochasticity >= 0.8 and expert = 1')
        for row in _c.fetchall():
            cases.append(dict((_c.description[i][0], value) for i, value in enumerate(row)))
    else:
        _c.execute('select * from main.cases where stochasticity >= 0.8')
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
                    statistics[str(original_solution) + str(original_solution)] += 1
                    break
        if initial is True and found is None:
            statistics[str(original_solution) + str(original_solution)] += 1

            if initial is not True:
                # verification per rules
                from absolute_validation import validation_per_rules
                if found is None:
                    for solution in POSSIBLE_SOLUTIONS:
                        test_case[SOLUTION] = solution
                        rules = validation_per_rules(test_case)
                        if rules[0]:
                            if solution == original_solution:
                                found = True
                                statistics[str(original_solution) + str(original_solution)] += 1
                                break
                            else:
                                found = False
                                statistics[str(original_solution) + str(rules[1])] += 1
                                break
                        elif not rules[0]:
                            if solution == original_solution:
                                statistics[str(original_solution) + str(rules[1])] += 1
                                found = False
                                break
                if found is None:
                    statistics[str(original_solution) + str(original_solution)] += 1

    print(statistics)
    return statistics


# # ------------------------------------------------------------------------------------------------------
# # I_NS_CB with similarity 0.8, add expert = true
# # R_NS_CB with similarity 0.8
def S_CB_Accuracy(initial):
    from segmentation import get_delegates_by_solution
    from case_segment_similarity import compare_case_delegate

    for test_case in test_cases:
        for possible_solution in POSSIBLE_SOLUTIONS:
            delegates = get_delegates_by_solution(possible_solution)
            for delegate in delegates:
                compare_case_delegate(test_case, delegate['delegate'])
    print(statistics)
    return statistics


NS_CB_Accuracy(False)
