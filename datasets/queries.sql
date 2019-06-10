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
                                           is (?, ?, ?, ?, ?) limit 1