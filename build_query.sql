CREATE TABLE IF NOT EXISTS climb_style (
	id SERIAL PRIMARY KEY,
	climb_style TEXT NOT NULL CONSTRAINT one_style UNIQUE)
	;
CREATE TABLE IF NOT EXISTS climbs (
	id SERIAL PRIMARY KEY,
	climb_name TEXT NOT NULL,
	url TEXT NOT NULL CONSTRAINT one_url UNIQUE,
	grade TEXT NOT NULL)
	;
CREATE TABLE IF NOT EXISTS style_guide (
    style INTEGER REFERENCES climb_style(id),
    climb_name INTEGER REFERENCES climbs(id),
    PRIMARY KEY (climb_name, style))
    ;
CREATE TABLE IF NOT EXISTS main_area (
	id SERIAL PRIMARY KEY,
	area TEXT NOT NULL CONSTRAINT one_area UNIQUE)
	;
CREATE TABLE IF NOT EXISTS sub_area (
	id SERIAL PRIMARY KEY,
	area TEXT NOT NULL,
	climb_id INTEGER REFERENCES climbs(id),
	area_id INTEGER REFERENCES main_area(id))
	;


--TODO: need to modify the database to add state and not duplicate for style regex
-- TODO: Modify existing databse to seperate style into style_guide table