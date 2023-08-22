# -- Auto Suspend
SHOW_WAREHOUSES = "show warehouses;"

WH_NOT_AUTOSUSPEND = """
select * from table(result_scan(last_query_id()))
where "auto_suspend" is null;
"""
