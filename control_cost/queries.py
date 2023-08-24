# -- Auto Suspend
SHOW_WAREHOUSES = 'show warehouses;'

WH_NOT_AUTOSUSPEND = """
select * from table(result_scan(last_query_id()))
where "auto_suspend" is null;
"""

COST_BY_WAREHOUSE = """
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
"""

COST_BY_ACCOUNT = """
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
"""

STATEMENT_TIMEOUTS = """
show parameters like 'STATE%' in account;
"""

GET_USERS = "show users;"

# DML from the information schema to identify table sizes and last updated timestamps
TABLES_SIZE = """
select table_catalog || '.' || table_schema || '.' || table_name as table_path, 
    table_name, table_schema as schema,
    table_catalog as database, bytes,
    to_number(bytes / power(1024,3),10,2) as gb, 
    last_altered as last_use,
    datediff('day',last_use,current_date) as days_since_last_use
from information_schema.tables
where days_since_last_use > 30 --use your days threshold
order by bytes desc;
"""

# TOP QUERY (TIME)
TOP_QUERIES = """
SELECT COUNT(QUERY_TEXT) TOTAL_EXECUTIONS, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '1 DAY'
GROUP BY QUERY_TEXT
ORDER BY TOTAL_EXECUTIONS DESC
LIMIT 10;
"""

TOP_QUERIES_TIME = """
SELECT TO_NUMBER(EXECUTION_TIME / 1000.0) EXECUTION_TIME_SEC, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '1 DAY'
ORDER BY EXECUTION_TIME_SEC DESC
LIMIT 10;
"""

TOP_QUERIES_QUEUE = """
SELECT QUEUED_OVERLOAD_TIME, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '1 DAY'
ORDER BY QUEUED_PROVISIONING_TIME DESC
LIMIT 10;
"""

TOP_QUERIES_PRICE = """
SELECT  CREDITS_USED_CLOUD_SERVICES, QUERY_TEXT
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= GETDATE() - INTERVAL '1 DAY'
ORDER BY CREDITS_USED_CLOUD_SERVICES DESC
LIMIT 10;
"""
