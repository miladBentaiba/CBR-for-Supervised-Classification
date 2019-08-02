"""This module segments the cases into three parts solution / problem / level."""

import sqlite3

import init
from constants import SOLUTION
from constants import ALL_FEATURES
from constants import POSSIBLE_SOLUTIONS
from Retrieve.case_segment_similarity import compare_case_delegate
from Retrieve.case_segment_similarity import get_level
from features_weights import Weighting

S = init.Singleton.get_instance()
WEIGHTS = Weighting.get_instance()


def create_segment(obj, iteration_number):
    """ create a new segment for the object obj and insert it """
    # last_insert_rowid() means incremental value of _id_segment
    # create the segment first
    cur = S.cursor()
    # print('insert into segment (?) values (?)')
    cur.execute('insert into segment ({0}) values (?)'.format(SOLUTION), (obj[SOLUTION],))
    # then, insert the case in the corresponding level of the segment
    # last_row_id means the last created segment
    _id_segment = cur.lastrowid
    # print('insert into cases_in_segment (_id_case, _id_segment, iteration) values (?,?,?)')
    cur.execute(
        'insert into cases_in_segment (_id_case, _id_segment, iteration) values '
        '(?,?,?)', (obj['_id_case'], _id_segment, iteration_number))
    S.commit()
    _deg = {'_id_segment': _id_segment, 'delegate': {}}
    for _x in ALL_FEATURES:
        if obj[_x] is not None:
            _deg['delegate'][_x] = [{'value': obj[_x], 'frequency': obj['frequency']}]
    return _deg


def insert_into_existing_segment(delegate, obj, iteration_number):
    """
    :param iteration_number: the number (rank) of the iteration
    :param delegate: delegate of the segment
    :param obj: a case
    :return: insert the case in the segment and return nothing
    """
    _c = S.cursor()
    # print('insert into cases_in_segment (_id_segment, _id_case, iteration, level) values (?,?,?,?)')
    _c.execute(
        'insert into cases_in_segment (_id_segment, _id_case, iteration, level) values (?,?,?,?)', (
            delegate['_id_segment'], obj['_id_case'], iteration_number, 1))
    S.commit()
    # updating the delegate
    for _x in ALL_FEATURES:
        # NOMINATIVE_FEATURES
        if _x[0] == 'c' and obj[_x] is not None:
            if _x not in delegate['delegate']:
                # feature _x is not mentioned in the delegate
                delegate['delegate'][_x] = [{'value': obj[_x], 'frequency': obj['frequency']}]
            elif not any(d['value'] == obj[_x] for d in delegate['delegate'][_x]):
                # feature _x is mentioned in the delegate, but the concerned value (obj[_x]) is not
                delegate['delegate'][_x].append({'value': obj[_x], 'frequency': obj['frequency']})
            else:
                # feature _x is mentioned in the delegate, and the concerned value (obj[_x]) is too
                # find the index of the dictionary where obj[_x] in mentioned
                index_v = next((index for (index, d) in
                                enumerate(delegate['delegate'][_x]) if d['value'] == obj[_x]), None)
                # update the frequency
                delegate['delegate'][_x][index_v]['frequency'] = obj['frequency']
        # quantitative features
        elif _x[0] == 'n':
            if obj[_x] is not None and _x not in delegate['delegate']:
                # the feature is not mentioned in the segment
                delegate['delegate'][_x] = [{'value': obj[_x], 'frequency': obj['frequency']}]
            elif obj[_x] is not None and _x in delegate['delegate']:
                # update the average of the quantitative feature
                sum_freq = delegate['delegate'][_x][0]['frequency'] + obj['frequency']
                feature_delegate = \
                    delegate['delegate'][_x][0]['value'] * delegate['delegate'][_x][0]['frequency']
                feature_obj = obj[_x] * obj['frequency']
                delegate['delegate'][_x][0]['value'] = (feature_delegate + feature_obj) / sum_freq
    return delegate


def get_delegates_by_solution(solution):
    """
    :param solution: thesolution of the segments
    :return: an array of _id_segment and its delegate. it has the following form:
    {'seg': 1, 'delegate': [{'feature': bi, 'value': 3, 'frequency': 4}, ...]}
    """
    _d = S.cursor()
    # print('select _id_segment from segment where ? = ?')
    _d.execute('select _id_segment from segment where ? = ?', (SOLUTION, solution))
    all_id_segments = _d.fetchall()
    structured_delegates = []
    for _id_segment in all_id_segments:
        _r = []
        for _x in ALL_FEATURES:
            if _x[0] == 'c':
                # print('select \'{0}\' as feature, {0} as value, '
                #       '      sum(frequency) as frequency '
                #       'from cases inner join cases_in_segment '
                #       '  on (cases._id_case = cases_in_segment._id_case) '
                #       '  inner join segment '
                #       '  on (cases_in_segment._id_segment = segment._id_segment) '
                #       'where cases_in_segment.level = 1 '
                #       '  and segment.{1} = ?1 '
                #       '  and segment._id_segment = ?2 '
                #       '  and {0} is not null '
                #       'group by value '
                #       .format(_x, SOLUTION), (solution, _id_segment[0]))
                _d.execute('select \'{0}\' as feature, {0} as value, '
                           '      sum(frequency) as frequency '
                           'from cases inner join cases_in_segment '
                           '  on (cases._id_case = cases_in_segment._id_case) '
                           '  inner join segment '
                           '  on (cases_in_segment._id_segment = segment._id_segment) '
                           'where cases_in_segment.level = 1 '
                           '  and segment.{1} = ?1 '
                           '  and segment._id_segment = ?2 '
                           '  and {0} is not null '
                           'group by value '
                           .format(_x, SOLUTION), (solution, _id_segment[0]))
                # _r is an array of the form {'feature': ,'value': , 'frequency': }
                # related only one feature and _id_segment
                for row in _d.fetchall():
                    _r.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
        # _deg is the delegate related to _id_segment and has the form of the example:
        # {'bi': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
        #  'margin': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
        #  'density': [{'value': 3, 'frequency': 4}]}
        _deg = dict()
        for row in _r:
            _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                            frequency=row['frequency']))
        _r2 = []
        for _x in ALL_FEATURES:
            if _x[0] == 'n':
                # print('select \'{0}\' as feature, avg({0}) as value, '
                #       '      sum(frequency) as frequency '
                #       'from cases inner join cases_in_segment '
                #       '  on (cases._id_case = cases_in_segment._id_case) '
                #       '  inner join segment '
                #       '  on (cases_in_segment._id_segment = segment._id_segment) '
                #       'where cases_in_segment.level = 1 '
                #       '  and segment.?3 = ?1 '
                #       '  and segment._id_segment = ?2 '
                #       '  and {0} is not null '
                #       'group by segment._id_segment '
                #       .format(_x))
                _d.execute('select \'{0}\' as feature, avg({0}) as value, '
                           '      sum(frequency) as frequency '
                           'from cases inner join cases_in_segment '
                           '  on (cases._id_case = cases_in_segment._id_case) '
                           '  inner join segment '
                           '  on (cases_in_segment._id_segment = segment._id_segment) '
                           'where cases_in_segment.level = 1 '
                           '  and segment.?3 = ?1 '
                           '  and segment._id_segment = ?2 '
                           '  and {0} is not null '
                           'group by segment._id_segment '
                           .format(_x), (solution, _id_segment[0], SOLUTION))
        for row in _d.fetchall():
            _r2.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
        for row in _r2:
            _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                            frequency=row['frequency']))
        # seg is the final delegate that contains all the needed information
        seg = {'_id_segment': _id_segment[0], 'delegate': _deg}
        structured_delegates.append(seg)
    return structured_delegates


def get_delegates():
    """
    :return: an array of _id_segment and its delegate. it has the following form:
    {'seg': 1, 'delegate': [{'feature': bi, 'value': 3, 'frequency': 4}, ...]}
    """
    _d = S.cursor()
    # print('select _id_segment, {0} from segment'.format(SOLUTION))
    _d.execute('select _id_segment, {0} from segment'.format(SOLUTION))
    all_id_segments = _d.fetchall()
    structured_delegates = []
    for _id_segment in all_id_segments:
        _r = []
        for _x in ALL_FEATURES:
            # NOMINATIVE_FEATURES
            if _x[0] == 'c':
                # print('select \'{0}\' as feature, {0} as value, '
                #       '      sum(frequency) as frequency '
                #       'from cases inner join cases_in_segment '
                #       '  on (cases._id_case = cases_in_segment._id_case) '
                #       '  inner join segment '
                #       '  on (cases_in_segment._id_segment = segment._id_segment) '
                #       'where cases_in_segment.level = 1 '
                #       '  and segment._id_segment = ? '
                #       '  and {0} is not null '
                #       'group by value '
                #       .format(_x), (_id_segment[0],))
                _d.execute('select \'{0}\' as feature, {0} as value, '
                           '      sum(frequency) as frequency '
                           'from cases inner join cases_in_segment '
                           '  on (cases._id_case = cases_in_segment._id_case) '
                           '  inner join segment '
                           '  on (cases_in_segment._id_segment = segment._id_segment) '
                           'where cases_in_segment.level = 1 '
                           '  and segment._id_segment = ? '
                           '  and {0} is not null '
                           'group by value '
                           .format(_x), (_id_segment[0],))
                # _r is an array of the form {'feature': ,'value': , 'frequency': }
                # related only one feature and _id_segment
                for row in _d.fetchall():
                    _r.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
        # _deg is the delegate related to _id_segment and has the form of the example:
        # {'bi': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
        #  'margin': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
        #  'density': [{'value': 3, 'frequency': 4}]}
        _deg = dict()
        for row in _r:
            _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                            frequency=row['frequency']))
        _r2 = []
        for _x in ALL_FEATURES:
            # quantitative features:
            if _x[0] == 'n':
                # print('select \'{0}\' as feature, avg({0}) as value, '
                #       '      sum(frequency) as frequency '
                #       'from cases inner join cases_in_segment '
                #       '  on (cases._id_case = cases_in_segment._id_case) '
                #       '  inner join segment '
                #       '  on (cases_in_segment._id_segment = segment._id_segment) '
                #       'where cases_in_segment.level = 1 '
                #       '  and segment._id_segment = ? '
                #       '  and {0} is not null '
                #       'group by segment._id_segment '
                #       .format(_x))
                _d.execute('select \'{0}\' as feature, avg({0}) as value, '
                           '      sum(frequency) as frequency '
                           'from cases inner join cases_in_segment '
                           '  on (cases._id_case = cases_in_segment._id_case) '
                           '  inner join segment '
                           '  on (cases_in_segment._id_segment = segment._id_segment) '
                           'where cases_in_segment.level = 1 '
                           '  and segment._id_segment = ? '
                           '  and {0} is not null '
                           'group by segment._id_segment '
                           .format(_x), (_id_segment[0],))
        for row in _d.fetchall():
            _r2.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
        for row in _r2:
            _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                            frequency=row['frequency']))
        # seg is the final delegate that contains all the needed information
        seg = {'_id_segment': _id_segment[0], 'delegate': _deg, SOLUTION: _id_segment[1]}
        structured_delegates.append(seg)
    return structured_delegates


def get_delegate(_id_segment):
    """
    :return: an array of _id_segment and its delegate. it has the following form:
    {'seg': 1, 'delegate': [{'feature': bi, 'value': 3, 'frequency': 4}, ...]}
    """
    _r = []
    _d = S.cursor()
    for _x in ALL_FEATURES:
        # nominative features
        if _x[0] == 'c':
            # print('select \'{0}\' as feature, {0} as value, '
            #       '      sum(frequency) as frequency '
            #       'from cases inner join cases_in_segment '
            #       '  on (cases._id_case = cases_in_segment._id_case) '
            #       '  inner join segment '
            #       '  on (cases_in_segment._id_segment = segment._id_segment) '
            #       'where cases_in_segment.level = 1 '
            #       # '  and cases.stochasticity >= 1 '
            #       '  and segment._id_segment = ? '
            #       '  and {0} is not null '
            #       'group by value '
            #       .format(_x))
            _d.execute('select \'{0}\' as feature, {0} as value, '
                       '      sum(frequency) as frequency '
                       'from cases inner join cases_in_segment '
                       '  on (cases._id_case = cases_in_segment._id_case) '
                       '  inner join segment '
                       '  on (cases_in_segment._id_segment = segment._id_segment) '
                       'where cases_in_segment.level = 1 '
                       # '  and cases.stochasticity >= 1 '
                       '  and segment._id_segment = ? '
                       '  and {0} is not null '
                       'group by value '
                       .format(_x), (_id_segment,))
            # _r is an array of the form {'feature': ,'value': , 'frequency': }
            # related only one feature and _id_segment
            for row in _d.fetchall():
                _r.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
    # _deg is the delegate related to _id_segment and has the form of the example:
    # {'bi': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
    #  'margin': [{'value': 5, 'frequency': 4}, {'value': 3, 'frequency': 2}],
    #  'density': [{'value': 3, 'frequency': 4}]}
    _deg = dict()
    for row in _r:
        _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                        frequency=row['frequency']))
    _r2 = []
    for _x in ALL_FEATURES:
        # quantitative features
        if _x[0] == 'n':
            # print(('select \'{0}\' as feature, avg({0}) as value, '
            #        '      sum(frequency) as frequency '
            #        'from cases inner join cases_in_segment '
            #        '  on (cases._id_case = cases_in_segment._id_case) '
            #        '  inner join segment '
            #        '  on (cases_in_segment._id_segment = segment._id_segment) '
            #        'where cases_in_segment.level = 1 '
            #        '  and segment._id_segment = ? '
            #        '  and {0} is not null '
            #        'group by segment._id_segment '
            #        .format(_x)))
            _d.execute('select \'{0}\' as feature, avg({0}) as value, '
                       '      sum(frequency) as frequency '
                       'from cases inner join cases_in_segment '
                       '  on (cases._id_case = cases_in_segment._id_case) '
                       '  inner join segment '
                       '  on (cases_in_segment._id_segment = segment._id_segment) '
                       'where cases_in_segment.level = 1 '
                       '  and segment._id_segment = ? '
                       '  and {0} is not null '
                       'group by segment._id_segment '
                       .format(_x), (_id_segment,))
    for row in _d.fetchall():
        _r2.append(dict((_d.description[i][0], value) for i, value in enumerate(row)))
    for row in _r2:
        _deg.setdefault(row['feature'], []).append(dict(value=row['value'],
                                                        frequency=row['frequency']))
    # seg is the final delegate that contains all the needed information
    seg = {'_id_segment': _id_segment, 'delegate': _deg}
    return seg


def segment_one(obj, iteration_number):
    """
    :param iteration_number: the number (rank) of the iteration
    :param obj: a case
    :return: segment one case and return nothing (find the corresponding segments and
    the corresponding levels in segments and insert the case. if no level equal to 1, create a
    segment for _it and store _it)
    """
    # boolean that indicates whether the case has been inserted in level one or not
    inserted_in_level_1 = False
    _c = S.cursor()
    # get delegates of all the concerned segments
    structured_delegates = get_delegates_by_solution(obj[SOLUTION])
    # save the case in only one segment (in its first level)
    for delegate in structured_delegates:
        similarity = compare_case_delegate(obj, delegate['delegate'], WEIGHTS)
        if get_level(similarity) == 1:
            inserted_in_level_1 = True
            try:
                insert_into_existing_segment(delegate,
                                             obj, iteration_number)
            except sqlite3.IntegrityError:
                print('obj already exists in the segment', obj)
            break
    if not inserted_in_level_1:
        create_segment(obj, iteration_number)


def segment_all(obj_array, iteration_number):
    """
    :param iteration_number: the number (rank) of the iteration
    :param obj_array: an array of cases
    :return: segment one case and return nothing (find the corresponding segments and
    the corresponding levels in segments and insert the case. if no level equal to 1, create a
    segment for _it and store _it)
    """
    # TODO divide obj_array according to obj's solutions
    for solutions in POSSIBLE_SOLUTIONS:
        # get delegates of all the concerned segments
        new_delegates = get_delegates_by_solution(solutions)
        for obj in obj_array:
            obj['segmented'] = False
            # if there is no segment
            if obj[SOLUTION] == solutions and not new_delegates:
                obj['segmented'] = True
                new_delegate = create_segment(obj, iteration_number)
                new_delegates.append(new_delegate)
            elif obj[SOLUTION] == solutions and new_delegates:
                i = 0
                # iterate over segments
                while i < len(new_delegates):
                    similarity = compare_case_delegate(obj, new_delegates[i]['delegate'], WEIGHTS)
                    if get_level(similarity) == 1:
                        obj['segmented'] = True
                        new_delegate = insert_into_existing_segment(new_delegates[i],
                                                                    obj, iteration_number)
                        new_delegates[i] = new_delegate
                        break
                    i += 1
                # if no segment fit the case (obj)
                if not obj['segmented']:
                    new_delegate = create_segment(obj, iteration_number)
                    new_delegates.append(new_delegate)
