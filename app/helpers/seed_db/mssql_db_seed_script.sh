#!/bin/bash

# **order matters here**
sql_files=(
    $mssql_create_db_file_name
    $mssql_create_tbls_file_name
)

sql_file_args=(
    $db_database
    $db_tbl_slider_data
    $db_tbl_slider_marks
    $db_schema
)

# condense ms sql query statements for sqlcmd
mssql_cmds_str="$mssql_cmd -S $db_server -U $db_username -P $db_password"

# create sql file arguments string -- include '$' symbol for referencing actual env var
sql_file_args_str=" "
for sql_file_arg in "${sql_file_args[@]}"; do
    sql_file_args_str+="${sql_file_arg}=\$${sql_file_arg} "
done

echo "***Using dev configuration***"
echo "***Waiting ${dev_db_seed_initial_wait} second(s) before attempting to scaffold the dev db***"
sleep $dev_db_seed_initial_wait
echo "Attempting to scaffold the dev db..."

# scaffold/prep the dev db for prd-like env
attempt=0
until [ $attempt -ge $dev_db_seed_max_attempt ] ; do
    # loop through sql file list and execute them via sqlcmd
    # -- if failure, move to next pause process and retry
    # -- if success, print message and break from loop
    for sql_file in "${sql_files[@]}"; do
        $mssql_cmds_str -v $sql_file_args_str -i "${mssql_seed_db_dir}/${sql_file}"
    done && echo "***Success: scaffolded dev db via SQL file(s)***" && break

    echo "***Waiting ${dev_db_seed_attempt_sleep_timer} seconds before new attempt to scaffold the dev db***"
    attempt=$((attempt+1))
    sleep $dev_db_seed_attempt_sleep_timer
done
