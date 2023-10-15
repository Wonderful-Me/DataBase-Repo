drop database if exists tmsys;
create database tmsys;
use tmsys;

# 创建教师表
create TABLE Teacher
	(Teacher_ID char(5) Primary Key,
     Teacher_name varchar(256),
     sex int,
     title int,
     Constraint csex check (sex in (1,2)), # sex 约束
     Constraint ctitle check (title > 0 and title < 12) # title 约束
	);

# 创建论文表
create TABLE Paper
	(Paper_ID int Primary Key,
     Paper_name varchar(256),
     Paper_src varchar(256),
     address_date Date,
     Paper_type int,
     level int,
     Constraint cptype check (Paper_type in (1,2,3,4)),
     Constraint cplevel check (level > 0 and level < 7)
	);

# 创建项目表
create TABLE Project
	(Project_ID varchar(256) Primary Key,
     Project_name varchar(256),
     Project_src varchar(256),
     Project_type int,
     funding float,
     start_year integer,
     end_year integer,
     Constraint cprotype check (Project_type > 0 and Project_type < 6)
	);

# 创建课程表
create TABLE Course
	(Course_ID varchar(256) Primary Key,
     Course_name varchar(256),
     Course_hour int,
     Course_type int,
     Constraint cctype check (Course_type in (1,2))
	);

# 发表论文关系
create TABLE Publish
	(Teacher_ID char(5),
     Paper_ID int,
     Pub_Rank int,
     coauth boolean,
     Constraint Publish_Teacher Foreign Key (Teacher_ID) references Teacher(Teacher_ID),
     Constraint Publish_Paper Foreign Key (Paper_ID) references Paper(Paper_ID)
	);

# 负责项目关系
create TABLE Incharge
	(Teacher_ID char(5),
     Project_ID varchar(256),
     Pro_Rank int,
     funding float,
     Constraint Charge_Teacher Foreign Key (Teacher_ID) references Teacher(Teacher_ID),
     Constraint Charge_Project Foreign Key (Project_ID) references Project(Project_ID)
	);

# 授课关系
create TABLE Teach
	(Teacher_ID char(5),
     Course_ID varchar(256),
     year int,
     semester int,
     teach_hour int,
     Constraint csemester check (semester in (1,2,3)),
     Constraint Teach_Teacher Foreign Key (Teacher_ID) references Teacher(Teacher_ID),
     Constraint Teach_Course Foreign Key (Course_ID) references Course(Course_ID)
	);

create TABLE User
	(User_Name Varchar(256) Primary Key,
     User_Password varchar(256)
	);