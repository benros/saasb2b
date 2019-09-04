*/ CREATE TABLE SF_LEAD */
create table sf_lead if not exists(
  id integer not null identity,
  isdeleted boolean,
  createddate timestamp,
  lastname varchar(16777216),
  firstname varchar(16777216),
  name varchar(16777216),
  title varchar(16777216),
  company varchar(16777216),
  leadsource varchar(16777216),
  email varchar(16777216),
  status varchar(16777216),
  industry varchar(16777216),
  currencyisocode varchar(16777216),
  ownerid number(38,0),
  converted varchar(16777216),
  isconverted number(38,0),
  convertedopportunityid varchar(16777216),
  convertedcontactid varchar(16777216),
  convertedaccountid varchar(16777216),
  referral_c varchar(16777216),
  wp_referrer_c varchar(16777216),
  lead_origin_c varchar(16777216),
  partner_c varchar(16777216)
);

/* CREATE TABLE PEOPLE */
CREATE TABLE people if not exists (
  id INTEGER NOT NULL IDENTITY,
  title varchar(16777216),
  lastname varchar(16777216),
  firstname varchar(16777216),
  email varchar(16777216)
);

/* CREATE TABLE SAASB2B_CONFIG */
CREATE TABLE saasb2b_config if not exists (
  id INTEGER NOT NULL IDENTITY,
  NAME varchar(16777216),
  INDUSTRY varchar(16777216),
  BILLINGCOUNTRY varchar(16777216),
  CURRENCYISOCODE varchar(16777216),
  ISDELETED varchar(16777216),
  number_of_leads integer,
  number_of_contacts integer,
  number_of_opportunities integer
);