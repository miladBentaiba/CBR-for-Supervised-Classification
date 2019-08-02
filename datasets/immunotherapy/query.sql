select
       (select sum(frequency) from cases where result_of_treatment=?1 and expert is 1) as s0,
       (select sum(frequency) from cases where ?2 in (0) and expert is 1) as s1,
       (select sum(frequency) from cases
         where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter, ?2, expert)
                  is (?,?,?,?,?,?,?, ?1, 1) ) as f0,
       (select sum(frequency) from cases
         where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter)
                   is (?,?,?,?,?,?,?) and ?2 in (0) and expert is 1) as f1;


select
    (select sum(frequency) from cases where result_of_treatment=?1 and expert is 1) as s0,
    (select sum(frequency) from cases where ?2 in (0) and expert is 1) as s1,
    (select sum(frequency) from cases
       where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter, ?2, expert)
                 is (?,?,?,?,?,?,?, ?1, 1) ) as f0,
    (select sum(frequency) from cases
       where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter)
                 is (?,?,?,?,?,?,?)
       and ?2 in (0) and expert is 1) as f1;

 (1, '1', 1, 15, 3, 2, 3, 900, 70)


select
   (select sum(frequency) from cases where {3}=?1 and expert is 1) as s0,
   (select sum(frequency) from cases where ?2 in (0) and expert is 1) as s1,
   (select sum(frequency) from cases where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter, ?2, expert)
                                               is ({2}, ?1, 1) ) as f0,
   (select sum(frequency) from cases where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter)
                                               is ({2}) and ?2 in (0) and expert is 1) as f1;
   .format(
   ",".join(map(str, _s1)), /**/
   ",".join(ALL_FEATURES),
   ",".join(['?'] * len(ALL_FEATURES)),
   SOLUTION)
select
(select sum(frequency) from cases where result_of_treatment=?1 and expert is 1) as s0,
(select sum(frequency) from cases where ?2 in (0) and expert is 1) as s1,
(select sum(frequency) from cases where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter, ?2, expert)
                                            is (?3,?4,?5,?6,?7, ?1, 1) ) as f0,
(select sum(frequency) from cases where (c_sex,n_age,n_time,n_number_of_warts,c_type,n_area,c_induration_diameter) is (?3,?4,?5,?6,?7)
                                    and ?2 in (0) and expert is 1) as f1
(1, '1', 1, 15, 3, 2, 3, 900, 70)
