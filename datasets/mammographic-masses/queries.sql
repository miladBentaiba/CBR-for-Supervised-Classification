CREATE TABLE IF NOT EXISTS cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    c_bi int check (c_bi in (0,1,2,3,4,5,6)),
    n_age int check (n_age <101),
    c_shape int check(c_shape in (1,2,3,4)),
    c_margin int check(c_margin in (1,2,3,4,5)),
    c_density int check (c_density in (1,2,3,4)),
    severity int check (severity in (0,1)), /* solution part */
    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/
    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */
    significance int DEFAULT null, /* a value used to calculate the stochastic validity */
    rule boolean DEFAULT null, /* is it valid according to rules? */
    expert boolean DEFAULT null, /* does the expert approved its validity? */
    randomized boolean not null default false,
    CONSTRAINT constraint_case UNIQUE (c_bi, n_age, c_shape, c_margin, c_density, severity)
);

CREATE TABLE IF NOT EXISTS weights
(
  feature text primary key not null, /* bi, age, shape, margin or density */
  weight integer not null /* its weight, maximum 1, minimum 0 */
);

insert into cases (c_bi, n_age, c_shape, c_margin, c_density, severity) values (5, 67, 3, 5, 3, 1);

select sum(frequency) from cases where (c_bi, n_age, c_shape, c_margin, c_density)
               is (?, ?, ?, ?, ?) limit 1;

select sum(frequency) from cases where (c_bi,n_age,c_shape,c_margin,c_density)
                                           is (?, ?, ?, ?, ?) limit 1;

with new (c_bi, n_age, c_shape, c_margin, c_density, severity, frequency, randomized, rule, expert)
    as (values (?, ?, ?, ?, ?, ?, 1, 0, 1, 1))
insert or replace into cases (_id_case, c_bi, n_age, c_shape, c_margin, c_density, severity, frequency,
                      randomness, significance, rule, expert, randomized)
select old._id_case, new.c_bi, new.n_age, new.c_shape, new.c_margin, new.c_density, new.severity,
       old.frequency + 1, old.randomness, old.significance, old.rule, new.expert, old.randomized
                   from new left join cases as old on
                       (new.c_bi, new.n_age, new.c_shape, new.c_margin, new.c_density, new.severity)
                       is (old.c_bi, old.n_age, old.c_shape, old.c_margin, old.c_density, old.severity);


with new (c_bi,n_age,c_shape,c_margin,c_density, severity, frequency, randomized, rule, expert)
    as ( values (?,?,?,?,?, ? , 1, 0, 1, 1))
    insert or replace into cases (_id_case, c_bi,n_age,c_shape,c_margin,c_density, severity,
                                  frequency, randomness, significance, rule,
                                  expert, randomized)
    select old._id_case, new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity, old.frequency + 1,
           old.randomness, old.significance, old.rule, new.expert, old.randomized
    from new left join cases as old on
        (new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity)
            is
        (old.c_bi,old.n_age,old.c_shape,old.c_margin,old.c_density, old.severity);


insert or ignore into rules (c_bi, ?2)
select distinct c_bi, ?2
from  (
    select distinct c_bi, ?2
    from cases
    where (c_bi) in (
        select c_bi
        from cases
        where expert = 1 and ?2 = ?1)
      and (c_bi) not in (
          select c_bi
          from cases
          where expert = 1 and ?2 <> ?1))
where 1  and c_bi is not null;


insert or ignore into rules (c_bi, ?2)
select distinct c_bi, ?2
from  (
    select distinct c_bi, ?2
    from cases
    where (c_bi) in (
        select c_bi
        from cases
        where expert = 1
          and severity = 0)
      and (c_bi) not in (
          select c_bi
          from cases
          where expert = 1
            and severity <> 0)  )
where 1
  and c_bi is not null;

select
       (select sum(frequency) from cases where severity=?1 and expert is 1) as s0,
       (select sum(frequency) from cases where ?2 in (0) and expert is 1) as s1,
       (select sum(frequency) from cases where (c_bi,n_age,c_shape,c_margin,c_density, ?2, expert)
                                                   is (?3,?4,?5,?6,?7, ?1, 1) ) as f0,
       (select sum(frequency) from cases where (c_bi,n_age,c_shape,c_margin,c_density)
                                                   is (?3,?4,?5,?6,?7) and ?2 in (0) and expert is 1) as f1;


with new (c_bi,n_age,c_shape,c_margin,c_density, severity, frequency, randomized, rule, expert)
    as ( values (5,49,4,5,3, 1 , 1, 0, null, 1))
insert or replace into cases (_id_case, c_bi,n_age,c_shape,c_margin,c_density, severity,
                              frequency, randomness, significance, rule, expert, randomized)
select old._id_case, new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity,
                              old.frequency + 1, old.randomness, old.significance, old.rule, new.expert,
       old.randomized
from new left join cases as old
on (new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity)
is (old.c_bi,old.n_age,old.c_shape,old.c_margin,old.c_density, old.severity);

select distinct * from cases;

with new (c_bi,n_age,c_shape,c_margin,c_density, severity, frequency, randomized, rule, expert)
as ( values (55,46,4,3,3, 1 , 1, 0, null, 1))
insert or replace into cases (_id_case, c_bi,n_age,c_shape,c_margin,c_density, severity, frequency, randomness,
                              significance, rule, expert, randomized)
select old._id_case, new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity, old.frequency + 1,
       old.randomness, old.significance, old.rule, new.expert, old.randomized
from new left join cases as old on (new.c_bi,new.n_age,new.c_shape,new.c_margin,new.c_density, new.severity)
                                is (old.c_bi,old.n_age,old.c_shape,old.c_margin,old.c_density, old.severity) ;

select sum(frequency) from cases;

select * from cases where rule is false;

select * from rules;

select c_bi, c_margin, c_density, c_shape, n_age from rules where c_bi = 0;

select distinct severity from rules
where 1
  and c_bi is 6
  and c_margin is null
  and c_density is null
  and c_shape is null
  and n_age is null;

select distinct severity
from rules
where 1
  and c_bi is 6
  and c_margin is 5
  and c_density is 3
  and c_shape is 4
  and n_age is null;

update cases set randomized = false;

update cases set segmented = 0;

select * from cases where segmented is false;

select * from cases where segmented = 1;

insert into test_cases
select _id_case, c_bi, n_age, c_shape, c_margin, c_density, severity from cases;

select * from main.cases where stochasticity >= 0.8 and expert = 1