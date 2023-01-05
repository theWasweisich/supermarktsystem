# Datenbank-Anwendung

## TABLE customers

&nbsp;
&nbsp;

***TABLE CREATE STATEMENT:***
`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,fname VARCHAR(255) NOT NULL,mname VARCHAR(255) DEFAULT NULL,lname VARCHAR(255) NOT NULL,visits INTEGER DEFAULT 1`

---

&nbsp;
&nbsp;

>***TABLE CONTENTS:***

&nbsp;

> Syntax: name; typ; bemerkung;

1. `id`; integer; wird automatisch hinzugefügt (Index);
2. `fname`; varchar(255); firstname, not null;
3. `mname`; varchar(255); middlename, default = null;
4. `lname`; varchar(255); lastname, not null;
5. `visits`; integer; wie oft schon kunde war, default 1;

> ***INSERT STATEMENT:***

`INSERT INTO users (fname, mname, lname, visits) VALUES (?first name?,?middle name?, ?last name?, ?visits?)`

*Hinweis: `mname` und `visits` sind optional :)*

&nbsp;
&nbsp;

---

---

&nbsp;
&nbsp;


## TABLE products

&nbsp;
&nbsp;

> ***TABLE CREATE STATEMENT:***

``CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0)``

&nbsp;

---

&nbsp;

> ***TABLE CONTENTS:***

&nbsp;

> Syntax: name; typ; bemerkung;

1. `id`; integer; wird automatisch hinzugefügt (Index);
2. `name`; varchar(255); Productname, not null;
3. `price`; integer; middlename, default = null;
4. `stock`; integer; Wie viel im Lager vorhandn ist., not null, default = 1;

&nbsp;
&nbsp;

---

&nbsp;
&nbsp;

> ***INSERT STATEMENT:***

&nbsp;

`INSERT INTO products (name, price, stock) VALUES (?Produktname?,?Produktpreis?, ?#Products in Stock?)`

*Hinweis: `stock` ist optional :)*