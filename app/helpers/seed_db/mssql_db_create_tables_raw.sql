use dev_db;
go

drop schema if exists dash_app;
go

drop table if exists dash_app.slider_data;
drop table if exists dash_app.slider_marks;
go

create schema dash_app

create table slider_data
(
    slider_id varchar not null primary key,
    slider_min float null,
    slider_max float null,
    slider_value float null,
    slider_step float null,
    tab_name_override_str varchar null
)

create table slider_marks
(
    row_id int identity(1,1) primary key,
    slider_id varchar not null foreign key references slider_data(slider_id),
    mark_value float not null
);
go