__author__ = 'sajive'
-- Table: public.agency

-- DROP TABLE public.agency;

CREATE TABLE public.agency
(
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone,
    deleted boolean,
    id varchar(36) NOT NULL,
    name character(50) COLLATE pg_catalog."default" NOT NULL,
    description character varying(256) COLLATE pg_catalog."default",
    status character(16) COLLATE pg_catalog."default",
    signup_ts date,    
    pancard character varying(10) COLLATE pg_catalog."default",
    rental_type integer,
    address1 character(50) COLLATE pg_catalog."default" NOT NULL,
    address2 character(50) COLLATE pg_catalog."default" NOT NULL,
    state character(16) COLLATE pg_catalog."default" NOT NULL,
    pincode integer NOT NULL,
    phone_office character(10) COLLATE pg_catalog."default" NOT NULL,
    contact_person character(50) COLLATE pg_catalog."default" NOT NULL,
    phone_mobile character(10) COLLATE pg_catalog."default" NOT NULL,
    city character(63) COLLATE pg_catalog."default",
    country character(63) COLLATE pg_catalog."default",
    CONSTRAINT agency_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.agency
    OWNER to postgres;

drop table bikes;

create table bikes (
bike_id varchar(36) NOT NULL,
agency_id int NOT NULL,
registration char(40) NOT NULL,
status char(10) NOT NULL,
model char(50) NOT NULL,
make char(50) NOT NULL,
year int NOT NULL,
last_service_date date NOT NULL,
cc int NOT NULL,
color char(10) NOT NULL,
total_km int NOT NULL,
fuel char(10) NOT NULL,
insurance char(16) NOT NULL,
riding_capacity int,
milage int,
PRIMARY KEY (bike_id),
FOREIGN KEY (agency_id) REFERENCES agency(id)
);


CREATE TABLE bike_additional_info (
id varchar(36) NOT NULL,
bike_id int NOT NULL,
image bytea NOT NULL,
type char(16) NOT NULL,
rpm char(10) NOT NULL,
gears int NOT NULL,
notes text NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
);


create table customers (
id varchar(36) NOT NULL,
first_name char(50) NOT NULL,
middle_name char(50),
last_name char(50) NOT NULL,
dob date NOT NULL,
address char(50) NOT NULL,
id_proof char(50) NOT NULL,
driving_license char(50) NOT NULL,
phone_mobile char(50) NOT NULL,
PRIMARY KEY (id)
);


create table rentals (
id varchar(36) NOT NULL,
bike_id int NOT NULL,
start_date date NOT NULL,
end_date date,
destination char(50) NOT NULL,
booking_ref char(32) NOT NULL,
booking_status char(16),
payment_status char(16),
customer_id int NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (bike_id) REFERENCES bikes(bike_id),
FOREIGN KEY (customer_id) REFERENCES customers(id)
);

create table payment_details (
id varchar(36) NOT NULL,
rental_id int NOT NULL,
payment_method int NOT NULL,
total_price int,
payment_date date,
notes text NOT NULL,
gst int,
pst int,
other_charges int,
discounts int,
PRIMARY KEY (id)
);

create table bike_pricing (
id varchar(36) NOT NULL,
bike_id int NOT NULL,
cost_per_day int NOT NULL,
start_date date,
end_date date,
notes text NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
);

create table agency_bike_pricing (
id varchar(36) NOT NULL,
bike_id int NOT NULL,
cost_per_day int NOT NULL,
start_date date,
end_date date,
status char(16) NOT NULL,
notes text NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
);
