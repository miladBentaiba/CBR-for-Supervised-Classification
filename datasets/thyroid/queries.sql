with new
    (n_t3_resin,n_total_serum_thyroxin,n_total_serum_triiodothyronine,n_TSH,n_difference_of_TSH,
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



