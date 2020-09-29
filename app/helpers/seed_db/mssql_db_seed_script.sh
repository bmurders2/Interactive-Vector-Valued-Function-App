#!/bin/bash

sql_files=(
    $mssql_create_db_file_name
    $mssql_create_tbls_file_name
)
# **order matters here
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

echo "Using dev configuration: attempting to seed the db for development..."
echo "Waiting ${sleep_timer} second(s) for the dev db to finish starting..."
sleep $sleep_timer

# loop through sql file list and execute them via sqlcmd
for sql_file in "${sql_files[@]}"; do
    $mssql_cmds_str -v $sql_file_args_str -i "${mssql_seed_db_dir}/${sql_file}"
done