CREATE DATABASE IF NOT EXISTS houm;
USE houm;
CREATE TABLE houm_markers (
    marker_id int NOT NULL AUTO_INCREMENT,
    lat decimal(10, 8),
    lon decimal(11, 8),
    houmer_id int NOT NULL,
    time_stamp datetime default current_timestamp,
    in_property INT DEFAULT 0,
    PRIMARY KEY (marker_id)
);
CREATE TABLE property_markers (
    property_id int NOT NULL,
    lat decimal(10, 8),
    lon decimal(11, 8),
    last_update datetime default current_timestamp,
    PRIMARY KEY (property_id)
);
CREATE TABLE houm_activity (
    houmer_id int NOT NULL,
    start_time datetime NOT NULL,
    end_time datetime NOT NULL,
    duration time,
    start_lat decimal(10, 8),
    start_lon decimal(11, 8),
    end_lat decimal(10, 8),
    end_lon decimal(11, 8),
    distance_m int,
    distance_km decimal(8, 1),
    velocity_km_hr decimal(8,1),
    PRIMARY KEY (houmer_id,start_time,end_time)
);

CREATE TABLE houm_in_property (
	in_property_id int NOT NULL AUTO_INCREMENT,
    houmer_id int NOT NULL,
    property_id int NOT NULL,
    houmer_marker_id int NOT NULL,
    time_stamp datetime default current_timestamp,
    PRIMARY KEY (in_property_id)
);

CREATE TABLE houm_in_property_activity (
	in_property_activity_id int NOT NULL AUTO_INCREMENT,
    start_time datetime,
    end_time datetime,
    duration time,
    houmer_id int NOT NULL,
    property_id int NOT NULL,
    PRIMARY KEY (in_property_activity_id)
);