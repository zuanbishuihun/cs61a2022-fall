.read data.sql


CREATE TABLE bluedog AS
  SELECT color,pet FROM students WHERE color="blue" AND pet="dog";

CREATE TABLE bluedog_songs AS
  SELECT color,pet,song FROM students WHERE color="blue" AND pet="dog";


CREATE TABLE smallest_int_having AS
  SELECT time,min(smallest) FROM students GROUP BY smallest HAVING count(*)=1;


CREATE TABLE matchmaker AS
  SELECT s1.pet,s1.song,s1.color,s2.color FROM students as s1,students as s2
    WHERE s1.time<s2.time AND s1.pet=s2.pet AND s1.song=s2.song; 


CREATE TABLE sevens AS
  SELECT seven FROM students,numbers WHERE students.time=numbers.time AND students.number=7 AND numbers."7"="True"; 


CREATE TABLE average_prices AS
  SELECT category,avg(MSRP) as average_price FROM products GROUP BY category;


CREATE TABLE lowest_prices AS
  SELECT store,item,price FROM inventory GROUP BY item HAVING min(price);

CREATE TABLE value_for_money AS -- 先算出每个item的代价 MSRP/rating 越小越好
  SELECT category,name,MSRP/rating AS cost FROM products;

CREATE TABLE shopping_list AS
  SELECT value_for_money.name,store FROM lowest_prices,value_for_money,products
    WHERE lowest_prices.item=products.name AND products.category=value_for_money.category AND products.name=value_for_money.name
      GROUP BY value_for_money.category
        HAVING min(value_for_money.cost);


CREATE TABLE total_bandwidth AS
  SELECT sum(Mbs) FROM shopping_list,stores 
    WHERE shopping_list.store=stores.store;

