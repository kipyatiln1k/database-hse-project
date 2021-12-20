
--functions & PROCEDURES


CREATE OR REPLACE PROCEDURE create_tables() AS $$
BEGIN
    CREATE TABLE city (
        city_id SERIAL NOT NULL PRIMARY KEY,
        city_name VARCHAR(50) NOT NULL UNIQUE
    );

    CREATE TABLE _storage (
        storage_id SERIAL PRIMARY KEY,
        city_id INT NOT NULL,
        total_shelfs_area INT DEFAULT 0 CHECK (total_shelfs_area >= 0),
        FOREIGN KEY (city_id) REFERENCES city (city_id) ON DELETE CASCADE
    );

    CREATE TABLE _owner (
        owner_id SERIAL NOT NULL PRIMARY KEY,
        owner_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(13) NOT NULL
    );

    CREATE TABLE item (
        item_id SERIAL NOT NULL PRIMARY KEY,
        item_name VARCHAR(255) NOT NULL,
        area INT CHECK (area > 0) NOT NULL,
        owner_id INT,
        FOREIGN KEY (owner_id) REFERENCES _owner (owner_id) ON DELETE SET NULL
    );

    CREATE TABLE shelf (
        shelf_id SERIAL NOT NULL PRIMARY KEY,
        storage_id INT NOT NULL,
        item_id INT,
        _number VARCHAR(25) NOT NULL UNIQUE,
        area INT NOT NULL CHECK(area > 0),
        FOREIGN KEY (storage_id) REFERENCES _storage (storage_id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES item (item_id) ON DELETE SET NULL
    );


    CREATE OR REPLACE FUNCTION total_shelfs_area_update()
    RETURNS trigger AS $total_shelfs_area_update$
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            UPDATE _storage st
            SET total_shelfs_area = st.total_shelfs_area - OLD.area + NEW.area
            WHERE st.storage_id = NEW.storage_id;
        ELSEIF (TG_OP = 'INSERT') THEN
            UPDATE _storage st
            SET total_shelfs_area = st.total_shelfs_area + NEW.area
            WHERE st.storage_id = NEW.storage_id;
        ELSEIF (TG_OP = 'DELETE') THEN
            UPDATE _storage st
            SET total_shelfs_area = st.total_shelfs_area - OLD.area
            WHERE st.storage_id = OLD.storage_id;
            RETURN OLD;
        END IF;
        RETURN NEW;
    END;
    $total_shelfs_area_update$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION check_shelf_area()
    RETURNS trigger AS $check_shelf_area$
    BEGIN
        IF (NEW.item_id IS NOT NULL AND (SELECT area FROM item WHERE item_id = NEW.item_id) > NEW.area) THEN
            RAISE EXCEPTION 'New shelf is too small for item on this';
        END IF;
        RETURN NEW;
    END;
    $check_shelf_area$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION check_item_area()
    RETURNS trigger AS $check_item_area$
    BEGIN
        IF (NEW.area > (SELECT area FROM shelf WHERE item_id = NEW.item_id)) THEN
            RAISE EXCEPTION 'New item is too large for it`s shelf';
        END IF;
    RETURN NEW;
    END;
    $check_item_area$ LANGUAGE plpgsql;


    CREATE OR REPLACE TRIGGER total_shelfs_area_update
        AFTER INSERT OR UPDATE OR DELETE ON shelf
        FOR EACH ROW
        EXECUTE PROCEDURE total_shelfs_area_update();

    CREATE OR REPLACE TRIGGER check_shelf_area
        BEFORE INSERT OR UPDATE ON shelf
        FOR EACH ROW
        EXECUTE PROCEDURE check_shelf_area();

    CREATE OR REPLACE TRIGGER check_item_area
        BEFORE INSERT OR UPDATE ON item
        FOR EACH ROW
        EXECUTE PROCEDURE check_item_area();
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE drop_database() AS $$
BEGIN
DROP DATABASE IF EXISTS storage_db; 
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION all_cityes()
RETURNS VARCHAR AS $$
BEGIN
	RETURN json_agg(tab.*) from city tab;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION all_owners()
RETURNS VARCHAR AS $$
BEGIN
	RETURN json_agg(tab.*) from _owner tab;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION all_items()
RETURNS VARCHAR AS $$
BEGIN
	RETURN json_agg(tab.*) from RETURN json_agg(tab.*) from (
        SELECT i.item_id, i.item_name, i.area, o.owner_name
        FROM item i JOIN _owners o ON i.owner_id = o.owner_id
        ) tab;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION all_storages()
RETURNS VARCHAR AS $$
BEGIN
	RETURN json_agg(tab.*) from (
        SELECT s.storage_id, c.city_name, s.total_shelfs_area
        FROM _storage s JOIN city c ON s.city_id = c.city_id
        ) tab;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION all_shelfs()
RETURNS VARCHAR AS $$
BEGIN
	RETURN json_agg(tab.*) FROM (
        SELECT s.shelf_id, s._number, s.storage_id, i.item_name, s.area
        FROM shelf s JOIN item i ON s.item_id = i.item_id) tab;
END;
$$ LANGUAGE plpgsql;


