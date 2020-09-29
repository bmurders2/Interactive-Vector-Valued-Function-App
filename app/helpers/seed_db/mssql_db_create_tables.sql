use $(db_database);
go

drop schema if exists $(db_schema);
go

drop table if exists $(db_schema).$(db_tbl_other_params);
drop table if exists $(db_schema).$(db_tbl_slider_marks);
drop table if exists $(db_schema).$(db_tbl_slider_data);
go

create schema $(db_schema)

create table $(db_tbl_other_params)
(
    row_id int identity(1,1) primary key,
    param_name nvarchar(100) not null,
    comp_id_str nvarchar(100) not null,
    value_str nvarchar(100) not null,
    additional_value_str nvarchar(100) null
)

create table $(db_tbl_slider_data)
(
    row_id int identity(1,1) primary key,
    slider_id nvarchar(100) not null unique,
    slider_min float null,
    slider_max float null,
    slider_value float null,
    slider_step float null,
    tab_name_override_str nvarchar(100) null
)

create table $(db_tbl_slider_marks)
(
    row_id int identity(1,1) primary key,
    slider_id nvarchar(100) not null,
    mark_value float not null
);
go