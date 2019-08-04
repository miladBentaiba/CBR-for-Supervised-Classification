with new
    (n_t3_resin,
    n_total_serum_thyroxin,
    n_total_serum_triiodothyronine,
    n_TSH,
    n_difference_of_TSH,
    class, frequency, randomized, rule, expert) as ( values (?,?,?,?,?, ? , 1, 0, null, 1))
insert or replace into cases
    (_id_case, n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,n_TSH,
     n_difference_of_TSH, class, frequency, randomness, significance, rule, expert, randomized)
select old._id_case, new.n_t3_resin,new.n_total_serum_thyroxin,new.n_total_serum_triiodothyronine,
       new.n_TSH,new.n_difference_of_TSH, new.class, old.frequency + 1, old.randomness, old.significance,
       old.rule, new.expert, old.randomized
from new
    left join cases as old
        on (new.n_t3_resin,new.n_total_serum_thyroxin,
            new.n_total_serum_triiodothyronine,new.n_TSH,
            new.n_difference_of_TSH, new.class)
               is
           (old.n_t3_resin,old.n_total_serum_thyroxin,old.n_total_serum_triiodothyronine,
            old.n_TSH,old.n_difference_of_TSH, old.class) ;
(1, 107, 10.1, 2.2, 0.9, 2.7)

insert into cases
    (n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,
     n_TSH,n_difference_of_TSH, class, frequency, randomness, significance,
     rule, expert, randomized)
values (1, 107, 10.1, 2.2, 0.9, 2.7, )

        (1, 107, 10.1, 2.2, 0.9, 2.7)

with new (n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,n_TSH,n_difference_of_TSH, class, frequency, randomized, rule, expert) as ( values (?,?,?,?,?, ? , 1, 0, null, 1)) insert or replace into cases (_id_case, n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,n_TSH,n_difference_of_TSH, class, frequency, randomness, significance, rule,                               expert, randomized) select old._id_case, new.n_t3_resin,new.n_total_serum_thyroxin,new.n_total_serum_triiodothyronine,new.n_TSH,new.n_difference_of_TSH, new.class, old.frequency + 1, old.randomness, old.significance,        old.rule, new.expert, old.randomized from new left join cases as old on (new.n_t3_resin,new.n_total_serum_thyroxin,new.n_total_serum_triiodothyronine,new.n_TSH,new.n_difference_of_TSH, new.class) is (old.n_t3_resin,old.n_total_serum_thyroxin,old.n_total_serum_triiodothyronine,old.n_TSH,old.n_difference_of_TSH, old.class)
(107, 10.1, 2.2, 0.9, 2.7)


with new (n_t3_resin, n_total_serum_thyroxin, n_total_serum_triiodothyronine, n_TSH, n_difference_of_TSH, class, frequency, randomized, rule, expert)
as ( values (107,     10.1,                   2.2,                            0.9,   2.7,                 1 ,    1,         0,          null, 1))
insert or replace into cases (_id_case, n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,n_TSH,n_difference_of_TSH, class,
                              frequency, randomness, significance, rule, expert, randomized)
select old._id_case, new.n_t3_resin,new.n_total_serum_thyroxin,new.n_total_serum_triiodothyronine,new.n_TSH,new.n_difference_of_TSH, new.class,
       old.frequency + 1, old.randomness, old.significance, old.rule, new.expert, old.randomized
from new left join cases as old
    on (new.n_t3_resin,new.n_total_serum_thyroxin,new.n_total_serum_triiodothyronine,new.n_TSH,new.n_difference_of_TSH, new.class)
           is (old.n_t3_resin,old.n_total_serum_thyroxin,old.n_total_serum_triiodothyronine,old.n_TSH,old.n_difference_of_TSH, old.class) ;
           (107, 10.1, 2.2, 0.9, 2.7, 1)




{'_id_case': 2, 'n_t3_resin': 113.0, 'n_total_serum_thyroxin': 9.9,
    'n_total_serum_triiodothyronine': 3.1, 'n_TSH': 2.0, 'n_difference_of_TSH': 5.9,
    'class': 1, 'randomness': 1, 'significance': 1, 'frequency': 1, 'stochasticity': 1,
    'rule': 1, 'segmented': False}
{'n_t3_resin': [{'value': 107.0, 'frequency': 1}],
'n_total_serum_thyroxin': [{'value': 10.1, 'frequency': 1}],
'n_total_serum_triiodothyronine': [{'value': 2.2, 'frequency': 1}],
'n_TSH': [{'value': 0.9, 'frequency': 1}],
'n_difference_of_TSH':
[{'value': 2.7, 'frequency': 1}]}
{'n_t3_resin': 0.8536993639102779,
'n_total_serum_thyroxin': 1,
'n_total_serum_triiodothyronine': 0,
'n_TSH': 0.7639772346836291,
'n_difference_of_TSH': 0.8195513893538667}


