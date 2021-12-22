FUNCTIONS_AND_PROCEDURES = {
    'create_database': """CREATE OR REPLACE PROCEDURE create_tables() AS $$
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
        item_id INT UNIQUE,
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
$$ LANGUAGE plpgsql;""",
    'create_functions': """CREATE OR REPLACE FUNCTION all_values(table_name VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    IF (table_name = 'city') THEN
        RETURN json_agg(tab.*) FROM city tab;
    ELSEIF (table_name = 'storage') THEN
        RETURN json_agg(tab.*) FROM (
            SELECT s.storage_id, c.city_name, s.total_shelfs_area
            FROM _storage s JOIN city c ON s.city_id = c.city_id
        ) tab;
    ELSEIF (table_name = 'owner') THEN
        RETURN json_agg(tab.*) FROM _owner tab;
    ELSEIF (table_name = 'item') THEN
        RETURN json_agg(tab.*) FROM (
            SELECT i.item_id, i.item_name, i.area, o.owner_name
            FROM item i JOIN _owner o ON i.owner_id = o.owner_id
        ) tab;
    ELSEIF (table_name = 'shelf') THEN
        RETURN json_agg(tab.*) FROM (
            SELECT s.shelf_id, s._number, s.storage_id, i.item_name, s.area
            FROM shelf s LEFT JOIN item i ON s.item_id = i.item_id
        ) tab;
    ELSE
        RAISE EXCEPTION 'There is no table %', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION count_values(table_name VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    IF (table_name = 'city') THEN
        RETURN COUNT(1) FROM city;
    ELSEIF (table_name = 'storage') THEN
        RETURN COUNT(1) FROM _storage;
    ELSEIF (table_name = 'owner') THEN
        RETURN COUNT(1) FROM _owner;
    ELSEIF (table_name = 'item') THEN
        RETURN COUNT(1) FROM item;
    ELSEIF (table_name = 'shelf') THEN
        RETURN COUNT(1) FROM shelf;
    ELSE
        RAISE EXCEPTION 'There is no table %', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_city(c_name VARCHAR) AS $$
BEGIN
	INSERT INTO city(city_name) VALUES (c_name);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_owner(o_name VARCHAR, o_phone VARCHAR) AS $$
BEGIN
	INSERT INTO _owner(owner_name, phone_number) VALUES (o_name, o_phone);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_item(i_name VARCHAR, i_owner_id INTEGER, i_area INTEGER) AS $$
BEGIN
	INSERT INTO item(item_name, owner_id, area) VALUES (i_name, i_owner_id, i_area);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_storage(s_city_id INTEGER) AS $$
BEGIN
	INSERT INTO _storage(city_id, total_shelfs_area) VALUES (s_city_id, 0);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_shelf(s_num VARCHAR, s_storage_id INTEGER, s_item_id INTEGER, s_area INTEGER) AS $$
BEGIN
	INSERT INTO shelf(_number, storage_id, item_id, area) VALUES (s_num, s_storage_id, s_item_id, s_area);
END;
$$ LANGUAGE plpgsql;


--UPDATE


CREATE OR REPLACE PROCEDURE update_city(id INTEGER, c_name VARCHAR) AS $$
BEGIN
	UPDATE city 
    SET city_name = c_name
    WHERE id = city_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_owner(id INTEGER, o_name VARCHAR, o_phone VARCHAR) AS $$
BEGIN
	UPDATE _owner
    SET owner_name = o_name, phone_number = o_phone
    WHERE id = owner_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_item(id INTEGER, i_name VARCHAR, i_owner_id INTEGER, i_area INTEGER) AS $$
BEGIN
	UPDATE item
    SET item_name = i_name, owner_id = i_owner_id, area = i_area
    WHERE id = item_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_storage(id INTEGER, s_city_id INTEGER) AS $$
BEGIN
	UPDATE _storage
    SET city_id = s_city_id
    WHERE id = storage_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_shelf(id INTEGER, s_num VARCHAR, s_storage_id INTEGER, s_item_id INTEGER, s_area INTEGER) AS $$
BEGIN
	UPDATE shelf
    SET _number = s_num, storage_id = s_storage_id, item_id = s_item, area = s_area
    WHERE id = shelf_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION search_value(table_name VARCHAR, _strict BOOLEAN, request VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    IF (table_name = 'city') THEN
        IF (_strict) THEN
            RETURN json_agg(tab.*) from (
                SELECT * 
                FROM city
                WHERE city.city_name = request
                ) tab;
        END IF;
        RETURN json_agg(tab.*) from (
            SELECT * 
            FROM city
            WHERE lower(city.city_name) LIKE CONCAT('%', lower(request), '%')
            ) tab;
    ELSEIF (table_name = 'owner') THEN
        IF (_strict) THEN
            RETURN json_agg(tab.*) FROM (
                SELECT * 
                FROM _owner
                WHERE _owner.owner_name = request
                ) tab;
        END IF;
        RETURN json_agg(tab.*) FROM (
            SELECT * 
            FROM _owner
            WHERE lower(_owner.owner_name) LIKE CONCAT('%', lower(request), '%')
            ) tab;
    ELSEIF (table_name = 'item') THEN
        IF (_strict) THEN
            RETURN json_agg(tab.*) FROM (
                SELECT * 
                FROM item
                WHERE item.item_name = request
                ) tab;
        END IF;
        RETURN json_agg(tab.*) FROM (
            SELECT * 
            FROM item
            WHERE lower(item.item_name) LIKE CONCAT('%', lower(request), '%')
            ) tab;
    ELSEIF (table_name = 'shelf') THEN
        IF (_strict) THEN
            RETURN json_agg(tab.*) FROM (
            SELECT * 
            FROM shelf
            WHERE shelf._number = request
            ) tab;
        END IF;
        RETURN json_agg(tab.*) FROM (
        SELECT * 
        FROM shelf
        WHERE lower(shelf._number) LIKE CONCAT('%', lower(request), '%')
        ) tab;
    ELSE
        RAISE EXCEPTION 'There is no table % or search is not available in the table', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE clear_table(TABLE_NAME VARCHAR) AS $$
BEGIN
	IF (table_name = 'city') THEN
        DELETE FROM city;
    ELSEIF (table_name = 'storage') THEN
        DELETE FROM _storage;
    ELSEIF (table_name = 'owner') THEN
        DELETE FROM _owner;
    ELSEIF (table_name = 'item') THEN
        DELETE FROM item;
    ELSEIF (table_name = 'shelf') THEN
        DELETE FROM shelf;
    ELSE
        RAISE EXCEPTION 'There is no table %', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE clear_tables() AS $$
BEGIN
    DELETE FROM city;
    DELETE FROM _storage;
    DELETE FROM _owner;
    DELETE FROM item;
    DELETE FROM shelf;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_by_id(TABLE_NAME VARCHAR, id INT) AS $$
BEGIN
	IF (table_name = 'city') THEN
        DELETE FROM city
        WHERE city_id = id;
    ELSEIF (table_name = 'storage') THEN
        DELETE FROM _storage
        WHERE storage_id = id;
    ELSEIF (table_name = 'owner') THEN
        DELETE FROM _owner
        WHERE owner_id = id;
    ELSEIF (table_name = 'item') THEN
        DELETE FROM item
        WHERE item_id = id;
    ELSEIF (table_name = 'shelf') THEN
        DELETE FROM shelf
        WHERE shelf_id = id;
    ELSE
        RAISE EXCEPTION 'There is no table %', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_by_index(TABLE_NAME VARCHAR, request VARCHAR) AS $$
BEGIN
	IF (table_name = 'city') THEN
        DELETE FROM city
        WHERE city_name = request;
    ELSEIF (table_name = 'owner') THEN
        DELETE FROM _owner
        WHERE owner_name = request;
    ELSEIF (table_name = 'item') THEN
        DELETE FROM item
        WHERE item_name = request;
    ELSEIF (table_name = 'shelf') THEN
        DELETE FROM shelf
        WHERE _number = request;
    ELSE
        RAISE EXCEPTION 'There is no table % or delete_by_index is not available in the table', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;""",
    'create_tables': 'CALL create_tables();',
    'all_values': "SELECT all_values('{table_name}');",
    'clear_table': "CALL clear_table('{table_name}');",
    'clear_tables': "CALL clear_tables();",
    'test_input': ["""CALL insert_city('Москва');
CALL insert_city('Питер');
CALL insert_city('Екат');""",
                   """CALL insert_storage(1);
CALL insert_storage(1);
CALL insert_storage(2);
CALL insert_storage(3);""",
                   """CALL insert_owner('ООО Екатэлектрострой', '88005553535');
CALL insert_owner('НИУ ВШЭ', '88005553535');""",
                   """CALL insert_item('Прах Бычкова', 2, 2);""",
                   """CALL insert_shelf('A1', 1, 1, 10);
CALL insert_shelf('A2', 1, NULL, 10);
CALL insert_shelf('A3', 2, NULL, 10);"""],
    'count_values': "SELECT count_values('{table_name}');",
    'insert_city': "CALL insert_city('{city_name}');",
    'insert_owner': "CALL insert_owner('{owner_name}, {phone_number}');",
    'insert_storage': "CALL insert_storage('{table_name}', '{city_name}');",
    'insert_item': "CALL insert_item('{table_name}', '{city_name}');",
    'insert_shelf': "CALL insert_shelf('{table_name}', '{city_name}');",
    'update_city': "CALL update_city({city_id},'{city_name}');",
    'update_owner': "CALL update_owner({owner_id},'{owner_name}, {phone_number}');",
    'update_storage': "CALL update_storage({city_id},'{table_name}', '{city_name}');",
    'update_item': "CALL update_item({city_id},'{table_name}', '{city_name}');",
    'update_shelf': "CALL update_shelf({city_id},'{table_name}', '{city_name}');",
    'delete_by_id': "CALL delete_by_id('{table}', {id})",
}
