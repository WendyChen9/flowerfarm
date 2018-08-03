-- auto-generated definition
create table CORDER
(
  OID     NUMBER not null,
  NAME    VARCHAR2(50),
  PHONE   VARCHAR2(50),
  ADDRESS VARCHAR2(50),
  WMICRO  NUMBER,
  MMICRO  NUMBER,
  CMICRO  NUMBER,
  HMICRO  NUMBER,
  BG      NUMBER,
  ODATE   VARCHAR2(50) default NULL,
  DDATE   VARCHAR2(50) default NULL
)
/

