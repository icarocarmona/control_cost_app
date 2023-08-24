---- CONTROLE DE CUSTO 

-- Auto Suspend
show warehouses;
select * from table(result_scan(last_query_id()))
where "auto_suspend" is null;


select * from snowflake.account_usage. 
order by 1 limit 10;



-- Auto Resume
show warehouses;
select * from table(result_scan(last_query_id()))
where "auto_resume" = false;

-- By Warehouse
with
cloudservices as (
    select
        warehouse_name
        ,month(start_time) as month
        ,sum(credits_used_cloud_services) as cloud_services_credits, 
        count(*) as no_querys 
    from
        snowflake.account_usage.query_history
    group by
        warehouse_name
        ,month
    order by
        warehouse_name
        ,no_querys desc
),
warehousemetering as (
    select
        warehouse_name
        ,month(start_time) as month
        ,sum(credits_used) as credits_for_month
    from
        snowflake.account_usage.warehouse_metering_history
    group by
        warehouse_name
        ,month
    order by
        warehouse_name
        ,credits_for_month desc
)
select
    *
    ,to_numeric(cloud_services_credits/nullif(credits_for_month,0)*100,10,2) as perct_cloud 
from
    cloudservices
join
    warehousemetering using(warehouse_name,month)
order by
    perct_cloud desc;



-- By Account
with
cloudservices as (
    select
        warehouse_name
        ,month(start_time) as month
        ,sum(credits_used_cloud_services) as cloud_services_credits, 
        count(*) as no_querys 
    from
        snowflake.account_usage.query_history
    group by
        warehouse_name
        ,month
    order by
        warehouse_name
        ,no_querys desc
),
warehousemetering as (
    select
        warehouse_name
        ,month(start_time) as month
        ,sum(credits_used) as credits_for_month
    from
        snowflake.account_usage.warehouse_metering_history
    group by
        warehouse_name
        ,month
    order by
        warehouse_name
        ,credits_for_month desc
)
select
    month
    ,sum(cloud_services_credits) as sum_cloud_services_credits
    ,sum(credits_for_month) as sum_credits_for_month
    ,to_numeric(sum_cloud_services_credits/nullif(sum_credits_for_month,0)*100,10,2) as perct_cloud 
from
    cloudservices
join
    warehousemetering using(warehouse_name,month)
group by
    month
order by
    perct_cloud desc;


-- Set statement timeouts for accounts and warehouses
show parameters like 'STATE%' in account;

alter account set STATEMENT_TIMEOUT_IN_SECONDS = 900;

show parameters in account;
-- Where the timeout is not the default value you’ve set
select * from table(result_scan(last_query_id()))
where "value" <> "default";

-- At the warehouse level
alter warehouse wh_dev_analyst set STATEMENT_TIMEOUT_IN_SECONDS = 1727;

show parameters in warehouse wh_dev_analyst;

show parameters in warehouse;
-- Never logged in
show users;
select * from table(result_scan(last_query_id()))
where "last_success_login" is null
and datediff('day',"created_on",current_date) > 90;

SELECT *  
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE datediff('day',"EVENT_TIMESTAMP",current_date) > 1;


SELECT NAME, DISPLAY_NAME FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
WHERE LAST_SUCCESS_LOGIN IS NULL
AND DELETED_ON IS NULL
AND DATEDIFF('DAY',CREATED_ON,CURRENT_DATE) > 90
AND NAME != 'SNOWFLAKE';

--and datediff('day',last_success_login,current_date) > 90


--Stale users more than 30 days
show users;
select *  from table(result_scan(last_query_id()))
where datediff('day',"last_success_login",current_date) > 90;

SELECT NAME, DISPLAY_NAME FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
where  DELETED_ON IS NULL
AND DATEDIFF('DAY',last_success_login,current_date) > 90
AND NAME != 'SNOWFLAKE';

---

SELECT distinct user_name
FROM snowflake.account_usage.login_history
WHERE user_name NOT IN (SELECT user_name 
                        FROM snowflake.account_usage.login_history 
                        WHERE event_timestamp > dateadd(day,-90,current_date())
                       )
AND event_type = 'LOGIN';
-- AND name != 'SNOWFLAKE';


SELECT distinct user_name
FROM snowflake.account_usage.login_history
WHERE user_name NOT IN (SELECT user_name 
                        FROM snowflake.account_usage.login_history 
                        WHERE event_timestamp > dateadd(day,-90,current_date())
                        AND event_type = 'LOGIN'
                       )
AND user_name NOT IN ('SNOWFLAKE', 'OKTA_CLIENT')
AND event_type = 'LOGIN';

SELECT distinct name
FROM snowflake.account_usage.users
WHERE name NOT IN (SELECT user_name 
                        FROM snowflake.account_usage.login_history 
                        WHERE event_timestamp > dateadd(day,-90,current_date())
                        AND event_type = 'LOGIN'
                       );




-- DML from the information schema to identify table sizes and last updated timestamps
select table_catalog || '.' || table_schema || '.' || table_name as table_path, 
    table_name, table_schema as schema,
    table_catalog as database, bytes,
    to_number(bytes / power(1024,3),10,2) as gb, 
    last_altered as last_use,
    datediff('day',last_use,current_date) as days_since_last_use
from information_schema.tables
where days_since_last_use > 30 --use your days threshold
order by bytes desc;
 
-- Last DML on object
select to_timestamp(to_varchar(
    system$last_change_commit_time('CREDIT_SAMPLE_BANK.PUBLIC.CREDIT_ASSESSMENTS')
    )) as LAST_DML_ON_OBJECT;
 
-- Queries on object in last 90 days
select count(*) from snowflake.account_usage.query_history
where contains(upper(query_text),'CREDIT_SAMPLE_BANK')
and datediff('day',start_time,current_date) < 90;

-----

ALTER SESSION SET TIMEZONE = 'America/Sao_Paulo';

set start_time='2023-07-01 00:00:00.000 -0300';

set end_time='2023-08-03 23:59:59.999 -0300';

 

WITH RECURSIVE

warehouse_history AS (

    select

        TO_DATE(DATE_TRUNC('day', start_time)) DATE,

        --warehouse_name,

        to_number(sum(credits_used),10,2) credits_used,

        to_number(sum(CREDITS_USED_COMPUTE),10,2) CREDITS_USED_COMPUTE,

        to_number(sum(CREDITS_USED_CLOUD_SERVICES),10,2) CREDITS_USED_CLOUD_SERVICES

    from snowflake.account_usage.warehouse_metering_history

    where start_time BETWEEN $start_time AND $end_time

    and warehouse_id not in ('0')

    --and warehouse_name = 'warehouse_name'

    group by DATE

    order by 1

    )

,

query_history AS (

    select

        TO_DATE(DATE_TRUNC('day', start_time)) DATE,

        warehouse_name,

        to_number(sum(TOTAL_ELAPSED_TIME) / 1000 / 60 , 10, 2) TOTAL_ELAPSED_TIME_MIN,

        to_number(max(TOTAL_ELAPSED_TIME) / 1000 / 60 , 10, 2) TOTAL_ELAPSED_TIME_MAX_MIN,

        to_number(sum(QUEUED_OVERLOAD_TIME) / 1000 / 60 , 10, 2) QUEUED_OVERLOAD_TIME_MIN,

        --to_number(sum(QUEUED_PROVISIONING_TIME) / 1000 / 60 , 10, 2) QUEUED_PROVISIONING_TIME_SEC,

        --to_number(sum(QUEUED_REPAIR_TIME) / 1000 / 60 , 10, 2) QUEUED_REPAIR_TIME_SEC,

        count(query_text) TOTAL_QUERY

    from snowflake.account_usage.query_history

    where start_time BETWEEN $start_time AND $end_time

    and warehouse_name is not null

    group by DATE,warehouse_name

    order by 1,2

)

select

    wh.date,

    --wh.warehouse_name,

    wh.credits_used

    --qry.total_elapsed_time_min,

    --qry.total_elapsed_time_max_min,

    --qry.queued_overload_time_min,

    --qry.total_query

    --CREDITS_USED_COMPUTE,

    --CREDITS_USED_CLOUD_SERVICES

from warehouse_history wh

left join query_history qry

    on wh.date = qry.date

    --and wh.warehouse_name = qry.warehouse_name

order by 1 desc

;


--
SELECT QUERY_TEXT, CREDITS_USED_CLOUD_SERVICES
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '1 DAY'
ORDER BY CREDITS_USED_CLOUD_SERVICES DESC
LIMIT 10;



SELECT QUEUED_OVERLOAD_TIME, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '30 DAY'
ORDER BY QUEUED_PROVISIONING_TIME DESC
LIMIT 10;


SELECT COUNT(QUERY_TEXT) TOTAL_EXECUTIONS, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '30 DAY'
GROUP BY QUERY_TEXT
ORDER BY TOTAL_EXECUTIONS DESC
LIMIT 10;
