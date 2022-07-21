use easybackups;
create table conexionssh(
id int PRIMARY KEY AUTO_INCREMENT,
IP VARCHAR(100) NOT NULL,
user varchar(100) NOT NULL,
pass varchar(100) NOT NULL
)
;
CREATE TABLE share(
id int primary key auto_increment,
origen varchar(150) NOT NULL,
final varchar(150) NOT NULL,
id_conexion int NOT NULL,
minutes varchar(30) not null,
hours varchar(30) not null,
days varchar(30) not null,
months varchar(30) not null,
weekday varchar(30) not null,
constraint FKid_conexion FOREIGN KEY(id_conexion) REFERENCES conexionssh(id)
);
