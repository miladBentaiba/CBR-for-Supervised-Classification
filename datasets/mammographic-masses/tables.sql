CREATE TABLE cases
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
    stochasticity int default null,
    CONSTRAINT constraint_case UNIQUE (c_bi, n_age, c_shape, c_margin, c_density, severity)
);

CREATE TABLE weights
(
  feature text primary key not null, /* c_bi, n_age, c_shape, c_margin or c_density */
  weight integer not null /* its weight, maximum 1, minimum 0 */
);

CREATE TABLE cases_in_segment
(
    _id integer PRIMARY KEY AUTOINCREMENT,
    _id_segment integer not null,
    _id_case integer not null,
    randomized boolean default false not null, /* has it been used to generate new cases or not yet */
    iteration int default 0 not null, /* in which iteration of randomization the case was generated*/
    level int check (level in (1,2,3,4,5)) not null default 1, /* level where the case is stored */
    FOREIGN KEY(_id_case) REFERENCES cases(_id_case)
);

CREATE TABLE segment
(
    _id_segment integer PRIMARY KEY autoincrement not null,
    severity int NOT NULL check (severity in (0,1)) /* severity of the cases stored in the segment */
);

Create table rules
(
  _id_rule integer primary key autoincrement not null,
  c_bi int check (c_bi in (0,1,2,3,4,5,6)) default null,
  n_age int check (n_age <101) default null,
  c_shape int check(c_shape in (1,2,3,4)) default null,
  c_margin int check(c_margin in (1,2,3,4,5)) default null,
  c_density int check (c_density in (1,2,3,4)) default null,
  severity int check (severity in (0,1)) not null, /* solution */
  CONSTRAINT constraint_rules_1 UNIQUE (c_bi, n_age, c_shape, c_margin, c_density)
);

CREATE TABLE test_cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    c_bi int check (c_bi in (0,1,2,3,4,5,6)),
    n_age int check (n_age <101),
    c_shape int check(c_shape in (1,2,3,4)),
    c_margin int check(c_margin in (1,2,3,4,5)),
    c_density int check (c_density in (1,2,3,4)),
    severity int check (severity in (0,1)) /* solution part */
);

CREATE TABLE new_cases
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
    segmented boolean not null default false,
    CONSTRAINT constraint_case UNIQUE (c_bi, n_age, c_shape, c_margin, c_density, severity)
);