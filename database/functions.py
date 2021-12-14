def create_function_query(function_name, arguments, return_datatype, return_variable_name,
                          declaration, queryes):
    return f"""CREATE OR REPLACE FUNCTION {function_name} ({", ".join(arguments)})
RETURNS {return_datatype} AS %{return_variable_name}%
DECLARE
""" + ";\n".join(declaration) + """
BEGIN
""" + ";\n".join(queryes) + """
RETURN {return_variable_name};
END;
LANGUAGE plpgsql;"""
    

def create_procedure_query(function_name, arguments, queryes):
    return f"""CREATE OR REPLACE PROCEDURE {function_name}({" ,".join(arguments)})
LANGUAGE SQL
AS $$
""" + "\n".join(queryes) + """
$$;"""


def create_trigger_query():
    pass


def create_table_query(table_name, fields):
    return f"""CREATE OR REPLACE TABLE {table_name} (
    """ + ",\n    ".join(fields) + """
);"""

TABLES = {
    'storage': {
        'table_name': 'storage',
        'fields': ['storage_id INT PRIMARY KEY AUTO_INCREMENT',
                   'city VARCHAR(255)',
                   'total_shelf_area INT',
                   'CHECK (total_shelf_area >= 0)']
    },
    'shelf': {
        'table_name': 'shelf',
        'fields': ['shelf_id INT PRIMARY KEY AUTO_INCREMENT',
                   'storage_id INT NOT NULL',
                   'item_id INT',
                   'number VARCHAR(25)',
                   'UNICUE (number)',
                   'area INT CHECK(area > 0)',
                   'FOREIGN KEY (storage_id) REFERENCES storage (storage_id) ON DELETE CASCADE',
                   'FOREIGN KEY (item_id) REFERENCES item (item_id) ON DELETE SET NULL']
    },
    'item': {
        'table_name': 'item',
        'fields': ['item_id INT PRIMARY KEY AUTO_INCREMENT',
                   'name VARCHAR(255)',
                   'area INT CHECK (area > 0)',
                   'owner_id INT NOT NULL',
                   'FOREIGN KEY (owner_id) REFERENCES owner (owner_id) ON DELETE SET NULL']
    },
    'owner': {
        'table_name': 'owner',
        'fields': ['owner_id INT PRIMARY KEY AUTO_INCREMENT',
                   'name VARCHAR(255)',
                   'phone_number VARCHAR(13)']
    }
}

PROCEDURES = {
    'create_tables': {
        'function_name': 'create_tables',
        'arguments': [],
        'queryes': [
            *[create_table_query(**table) for table in TABLES.values()]
        ]
    }
}    

if __name__ == '__main__':
    print(create_table_query(**TABLES['item']))