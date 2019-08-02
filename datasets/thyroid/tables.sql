CREATE TABLE cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    n_t3_resin int,
    n_total_serum_thyroxin int,
    n_total_serum_triiodothyronine int,
    n_TSH int,
    n_difference_of_TSH int,
    class int check (class in (1,2,3)), /* solution part */
    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/
    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */
    significance int DEFAULT null, /* a value used to calculate the stochastic validity */
    rule boolean DEFAULT null, /* is it valid according to rules? */
    expert boolean DEFAULT null, /* does the expert approved its validity? */
    randomized boolean not null default false,
    stochasticity int default null,
    segmented boolean not null default false,
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
    class int NOT NULL check (severity in (1,2,3)) /* severity of the cases stored in the segment */
);

Create table rules
(
  _id_rule integer primary key autoincrement not null,
  n_t3_resin int,
  n_total_serum_thyroxin int,
  n_total_serum_triiodothyronine int,
  n_TSH int,
  n_difference_of_TSH int,
  class int check (class in (1,2,3)), /* solution part */
  CONSTRAINT constraint_rules_1 UNIQUE (n_t3_resin, n_total_serum_thyroxin, n_total_serum_triiodothyronine,
     n_TSH, n_difference_of_TSH)
);

CREATE TABLE test_cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    n_t3_resin int,
  n_total_serum_thyroxin int,
  n_total_serum_triiodothyronine int,
  n_TSH int,
  n_difference_of_TSH int,
  class int check (class in (1,2,3)), /* solution part */
);

CREATE TABLE new_cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    n_t3_resin int,
    n_total_serum_thyroxin int,
    n_total_serum_triiodothyronine int,
    n_TSH int,
    n_difference_of_TSH int,
    class int check (class in (1,2,3)), /* solution part */
    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/
    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */
    significance int DEFAULT null, /* a value used to calculate the stochastic validity */
    rule boolean DEFAULT null, /* is it valid according to rules? */
    expert boolean DEFAULT null, /* does the expert approved its validity? */
    randomized boolean not null default false,
    segmented boolean not null default false,
    CONSTRAINT constraint_case UNIQUE (n_t3_resin, n_total_serum_thyroxin, n_total_serum_triiodothyronine,
  n_TSH, n_difference_of_TSH, class)
);