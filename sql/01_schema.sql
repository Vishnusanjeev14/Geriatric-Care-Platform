-- CareConnect V2 MySQL schema
-- Generated from SQLAlchemy models. Keep this in sync with migrations.

SET NAMES utf8mb4;
USE `careconnect_v2`;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `medicine_adherence`;
DROP TABLE IF EXISTS `medicine_schedules`;
DROP TABLE IF EXISTS `medicine_order_items`;
DROP TABLE IF EXISTS `inventory_items`;
DROP TABLE IF EXISTS `care_requests`;
DROP TABLE IF EXISTS `timeline_events`;
DROP TABLE IF EXISTS `profile_addresses`;
DROP TABLE IF EXISTS `prescriptions`;
DROP TABLE IF EXISTS `notifications`;
DROP TABLE IF EXISTS `medicines`;
DROP TABLE IF EXISTS `medicine_orders`;
DROP TABLE IF EXISTS `medical_conditions`;
DROP TABLE IF EXISTS `home_service_bookings`;
DROP TABLE IF EXISTS `emergency_contacts`;
DROP TABLE IF EXISTS `caretakers`;
DROP TABLE IF EXISTS `appointments`;
DROP TABLE IF EXISTS `account_profile_permissions`;
DROP TABLE IF EXISTS `profiles`;
DROP TABLE IF EXISTS `medicine_categories`;
DROP TABLE IF EXISTS `hospitals`;
DROP TABLE IF EXISTS `accounts`;

SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE accounts (
	full_name VARCHAR(120) NOT NULL, 
	email VARCHAR(180) NOT NULL, 
	phone VARCHAR(30), 
	password_hash VARCHAR(255) NOT NULL, 
	account_type VARCHAR(40) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	preferred_language VARCHAR(8) NOT NULL, 
	last_login_at DATETIME, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);


CREATE TABLE hospitals (
	name VARCHAR(160) NOT NULL, 
	branch_type VARCHAR(40) NOT NULL, 
	address VARCHAR(255), 
	city VARCHAR(80) NOT NULL, 
	distance_km NUMERIC(5, 1) NOT NULL, 
	rating NUMERIC(3, 1) NOT NULL, 
	departments VARCHAR(255) NOT NULL, 
	latitude NUMERIC(10, 6), 
	longitude NUMERIC(10, 6), 
	phone VARCHAR(40), 
	emergency_available BOOL NOT NULL, 
	working_hours VARCHAR(120), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);


CREATE TABLE medicine_categories (
	name VARCHAR(100) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);


CREATE TABLE profiles (
	display_name VARCHAR(120) NOT NULL, 
	relationship_label VARCHAR(80) NOT NULL, 
	date_of_birth DATE NOT NULL, 
	gender VARCHAR(40), 
	photo_initials VARCHAR(4) NOT NULL, 
	blood_group VARCHAR(5), 
	health_status VARCHAR(40) NOT NULL, 
	primary_hospital VARCHAR(160), 
	primary_care_note TEXT, 
	status VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);


CREATE TABLE account_profile_permissions (
	account_id INTEGER NOT NULL, 
	profile_id INTEGER NOT NULL, 
	`role` VARCHAR(40) NOT NULL, 
	accepted_at DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_account_profile UNIQUE (account_id, profile_id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id)
);


CREATE TABLE appointments (
	profile_id INTEGER NOT NULL, 
	booked_by_account_id INTEGER NOT NULL, 
	hospital_id INTEGER NOT NULL, 
	appointment_date DATE NOT NULL, 
	appointment_time VARCHAR(20) NOT NULL, 
	reason VARCHAR(180) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(booked_by_account_id) REFERENCES accounts (id), 
	FOREIGN KEY(hospital_id) REFERENCES hospitals (id)
);


CREATE TABLE caretakers (
	account_id INTEGER NOT NULL, 
	specialties VARCHAR(180) NOT NULL, 
	languages VARCHAR(120) NOT NULL, 
	rating NUMERIC(3, 1) NOT NULL, 
	available BOOL NOT NULL, 
	experience_years INTEGER NOT NULL, 
	verified BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id)
);


CREATE TABLE emergency_contacts (
	profile_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	relationship VARCHAR(80) NOT NULL, 
	phone VARCHAR(30) NOT NULL, 
	priority INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id)
);


CREATE TABLE home_service_bookings (
	profile_id INTEGER NOT NULL, 
	booked_by_account_id INTEGER NOT NULL, 
	service_type VARCHAR(80) NOT NULL, 
	scheduled_date DATE NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(booked_by_account_id) REFERENCES accounts (id)
);


CREATE TABLE medical_conditions (
	profile_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	severity VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id)
);


CREATE TABLE medicine_orders (
	profile_id INTEGER NOT NULL, 
	ordered_by_account_id INTEGER NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	total_amount NUMERIC(10, 2) NOT NULL, 
	delivery_address VARCHAR(255) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(ordered_by_account_id) REFERENCES accounts (id)
);


CREATE TABLE medicines (
	category_id INTEGER NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	generic_name VARCHAR(160), 
	strength VARCHAR(80) NOT NULL, 
	form VARCHAR(60) NOT NULL, 
	brand VARCHAR(120), 
	pack_size VARCHAR(80) NOT NULL, 
	manufacturer VARCHAR(120) NOT NULL, 
	unit_price NUMERIC(10, 2) NOT NULL, 
	requires_prescription BOOL NOT NULL, 
	stock_remaining INTEGER NOT NULL, 
	minimum_stock INTEGER NOT NULL, 
	barcode VARCHAR(80), 
	expiry_placeholder VARCHAR(20), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES medicine_categories (id)
);


CREATE TABLE notifications (
	account_id INTEGER NOT NULL, 
	profile_id INTEGER, 
	category VARCHAR(60) NOT NULL, 
	priority VARCHAR(40) NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	message TEXT NOT NULL, 
	read_at DATETIME, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id)
);


CREATE TABLE prescriptions (
	profile_id INTEGER NOT NULL, 
	uploaded_by_account_id INTEGER NOT NULL, 
	original_filename VARCHAR(180) NOT NULL, 
	extracted_text TEXT, 
	status VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(uploaded_by_account_id) REFERENCES accounts (id)
);


CREATE TABLE profile_addresses (
	profile_id INTEGER NOT NULL, 
	label VARCHAR(80) NOT NULL, 
	line1 VARCHAR(180) NOT NULL, 
	city VARCHAR(80) NOT NULL, 
	state VARCHAR(80) NOT NULL, 
	postal_code VARCHAR(20) NOT NULL, 
	is_default BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id)
);


CREATE TABLE timeline_events (
	profile_id INTEGER NOT NULL, 
	actor_account_id INTEGER, 
	event_type VARCHAR(80) NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	description TEXT NOT NULL, 
	source_module VARCHAR(80) NOT NULL, 
	priority VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(actor_account_id) REFERENCES accounts (id)
);


CREATE TABLE care_requests (
	profile_id INTEGER NOT NULL, 
	requested_by_account_id INTEGER NOT NULL, 
	caretaker_id INTEGER, 
	care_type VARCHAR(60) NOT NULL, 
	start_date DATE NOT NULL, 
	visit_time VARCHAR(20) NOT NULL, 
	duration VARCHAR(80) NOT NULL, 
	language VARCHAR(80), 
	gender_preference VARCHAR(40), 
	recurring BOOL NOT NULL, 
	emergency_request BOOL NOT NULL, 
	notes TEXT, 
	status VARCHAR(40) NOT NULL, 
	visit_note TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(requested_by_account_id) REFERENCES accounts (id), 
	FOREIGN KEY(caretaker_id) REFERENCES caretakers (id)
);


CREATE TABLE inventory_items (
	medicine_id INTEGER NOT NULL, 
	branch_name VARCHAR(160) NOT NULL, 
	quantity_on_hand INTEGER NOT NULL, 
	reorder_level INTEGER NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(medicine_id) REFERENCES medicines (id)
);


CREATE TABLE medicine_order_items (
	order_id INTEGER NOT NULL, 
	medicine_id INTEGER NOT NULL, 
	medicine_name_snapshot VARCHAR(160) NOT NULL, 
	quantity INTEGER NOT NULL, 
	unit_price_snapshot NUMERIC(10, 2) NOT NULL, 
	line_total NUMERIC(10, 2) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES medicine_orders (id), 
	FOREIGN KEY(medicine_id) REFERENCES medicines (id)
);


CREATE TABLE medicine_schedules (
	profile_id INTEGER NOT NULL, 
	medicine_id INTEGER NOT NULL, 
	dosage_text VARCHAR(160) NOT NULL, 
	timing_text VARCHAR(160) NOT NULL, 
	start_date DATE, 
	end_date DATE, 
	forever_medication BOOL NOT NULL, 
	times_per_day INTEGER NOT NULL, 
	dose_morning BOOL NOT NULL, 
	dose_afternoon BOOL NOT NULL, 
	dose_evening BOOL NOT NULL, 
	dose_night BOOL NOT NULL, 
	food_timing VARCHAR(40) NOT NULL, 
	quantity_per_dose VARCHAR(40) NOT NULL, 
	unit VARCHAR(40) NOT NULL, 
	repeat_pattern VARCHAR(40) NOT NULL, 
	repeat_days VARCHAR(80), 
	notes TEXT, 
	adherence_percent INTEGER NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(medicine_id) REFERENCES medicines (id)
);


CREATE TABLE medicine_adherence (
	schedule_id INTEGER NOT NULL, 
	profile_id INTEGER NOT NULL, 
	dose_date DATE NOT NULL, 
	dose_period VARCHAR(40) NOT NULL, 
	dose_time VARCHAR(20) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	confirmed_by_account_id INTEGER, 
	notes TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(schedule_id) REFERENCES medicine_schedules (id), 
	FOREIGN KEY(profile_id) REFERENCES profiles (id), 
	FOREIGN KEY(confirmed_by_account_id) REFERENCES accounts (id)
);

CREATE INDEX ix_accounts_status ON accounts (status);
CREATE INDEX ix_accounts_account_type ON accounts (account_type);
CREATE UNIQUE INDEX ix_accounts_email ON accounts (email);
CREATE INDEX ix_profiles_display_name ON profiles (display_name);
CREATE INDEX ix_account_profile_permissions_account_id ON account_profile_permissions (account_id);
CREATE INDEX ix_account_profile_permissions_profile_id ON account_profile_permissions (profile_id);
CREATE INDEX ix_appointments_status ON appointments (status);
CREATE INDEX ix_appointments_profile_id ON appointments (profile_id);
CREATE INDEX ix_emergency_contacts_profile_id ON emergency_contacts (profile_id);
CREATE INDEX ix_home_service_bookings_status ON home_service_bookings (status);
CREATE INDEX ix_home_service_bookings_profile_id ON home_service_bookings (profile_id);
CREATE INDEX ix_medical_conditions_profile_id ON medical_conditions (profile_id);
CREATE INDEX ix_medicine_orders_status ON medicine_orders (status);
CREATE INDEX ix_medicine_orders_profile_id ON medicine_orders (profile_id);
CREATE INDEX ix_medicines_name ON medicines (name);
CREATE INDEX ix_medicines_category_id ON medicines (category_id);
CREATE INDEX ix_notifications_profile_id ON notifications (profile_id);
CREATE INDEX ix_notifications_account_id ON notifications (account_id);
CREATE INDEX ix_prescriptions_status ON prescriptions (status);
CREATE INDEX ix_prescriptions_profile_id ON prescriptions (profile_id);
CREATE INDEX ix_profile_addresses_profile_id ON profile_addresses (profile_id);
CREATE INDEX ix_timeline_events_event_type ON timeline_events (event_type);
CREATE INDEX ix_timeline_events_profile_id ON timeline_events (profile_id);
CREATE INDEX ix_care_requests_profile_id ON care_requests (profile_id);
CREATE INDEX ix_care_requests_status ON care_requests (status);
CREATE INDEX ix_inventory_items_medicine_id ON inventory_items (medicine_id);
CREATE INDEX ix_medicine_order_items_order_id ON medicine_order_items (order_id);
CREATE INDEX ix_medicine_schedules_profile_id ON medicine_schedules (profile_id);
CREATE INDEX ix_medicine_adherence_profile_id ON medicine_adherence (profile_id);
CREATE INDEX ix_medicine_adherence_dose_date ON medicine_adherence (dose_date);
CREATE INDEX ix_medicine_adherence_schedule_id ON medicine_adherence (schedule_id);
