CREATE TABLE IF NOT EXISTS cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    bi int check (bi in (0,1,2,3,4,5,6)),
    age int check (age <101),
    shape int check(shape in (1,2,3,4)),
    margin int check(margin in (1,2,3,4,5)),
    density int check (density in (1,2,3,4)),
    severity int check (severity in (0,1)), /* solution part */
    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/
    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */
    significance int DEFAULT null, /* a value used to calculate the stochastic validity */
    rule boolean DEFAULT null, /* is it valid according to rules? */
    expert boolean DEFAULT null, /* does the expert approved its validity? */
    randomized boolean not null default false,
    stochasticity int default null,
    CONSTRAINT constraint_case UNIQUE (bi, age, shape, margin, density, severity)
);

CREATE TABLE IF NOT EXISTS weights
(
  feature text primary key not null, /* bi, age, shape, margin or density */
  weight integer not null /* its weight, maximum 1, minimum 0 */
);

CREATE TABLE IF NOT EXISTS cases_in_segment
(
    _id integer PRIMARY KEY AUTOINCREMENT,
    _id_segment integer not null,
    _id_case integer not null,
    randomized boolean default false not null, /* has it been used to generate new cases or not yet */
    iteration int default 0 not null, /* in which iteration of randomization the case was generated*/
    level int check (level in (1,2,3,4,5)) not null default 1, /* level where the case is stored */
    FOREIGN KEY(_id_case) REFERENCES cases(_id_case)
);

CREATE TABLE IF NOT EXISTS segment
(
    _id_segment integer PRIMARY KEY autoincrement not null,
    severity int NOT NULL check (severity in (0,1)) /* severity of the cases stored in the segment */
);

Create table IF NOT EXISTS rules
(
  _id_rule integer primary key autoincrement not null,
  bi int check (bi in (0,1,2,3,4,5,6)) default null,
  age int check (age <101) default null,
  shape int check(shape in (1,2,3,4)) default null,
  margin int check(margin in (1,2,3,4,5)) default null,
  density int check (density in (1,2,3,4)) default null,
  severity int check (severity in (0,1)) not null, /* solution */
  CONSTRAINT constraint_rules_1 UNIQUE (bi, age, shape, margin, density)
);

CREATE TABLE IF NOT EXISTS test_cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    bi int check (bi in (0,1,2,3,4,5,6)),
    age int check (age <101),
    shape int check(shape in (1,2,3,4)),
    margin int check(margin in (1,2,3,4,5)),
    density int check (density in (1,2,3,4)),
    severity int check (severity in (0,1)) /* solution part */
);

CREATE TABLE IF NOT EXISTS new_cases
(
    _id_case integer PRIMARY KEY AUTOINCREMENT,
    bi int check (bi in (0,1,2,3,4,5,6)),
    age int check (age <101),
    shape int check(shape in (1,2,3,4)),
    margin int check(margin in (1,2,3,4,5)),
    density int check (density in (1,2,3,4)),
    severity int check (severity in (0,1)), /* solution part */
    frequency int DEFAULT 1 NOT NULL, /* number of times the case exists*/
    randomness int DEFAULT null, /* a value used to calculate the stochastic validity */
    significance int DEFAULT null, /* a value used to calculate the stochastic validity */
    rule boolean DEFAULT null, /* is it valid according to rules? */
    expert boolean DEFAULT null, /* does the expert approved its validity? */
    randomized boolean not null default false,
    CONSTRAINT constraint_case UNIQUE (bi, age, shape, margin, density, severity)
);