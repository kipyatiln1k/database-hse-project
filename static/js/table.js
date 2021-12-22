"use strict";

async function selector(table, field) {
    selector = document.createElement("select");
    selector.className = "form-select";
    let response = await fetch(
        Flask.url_for("tables.get_values", { table_name: table })
    );

    if (response.ok) {
        let json = await response.json();

        for (element in json) {
            let option = document.createElement("option");
            option.value = element[`${table}_id`];
            option.innerText = element[field];
            selector.appendChild(option);
        }

        return selector;
    } else {
        return null;
    }
}

function text_field(placeholder = "") {
    let text = document.createElement("input");
    text.className = "form-control";
    text.placeholder = placeholder;
    text.for;

    return text;
}

function create_table() {
    let head = document.getElementById("thead");
    let row = document.createElement("tr");

    let th = document.createElement("th");
    row.appendChild(th);
    for (let field_name of fields_names) {
        let th = document.createElement("th");
        th.innerText = field_name;
        row.appendChild(th);
    }
    th = document.createElement("th");
    row.appendChild(th);

    head.appendChild(row);

    update_table();
}

function add_form(row, prefix = "new", element = null) {
    for (let field of fields) {
        let td = document.createElement("td");
        if (field in forms) {
            switch (forms[field]) {
                case "text":
                    let txt_field = text_field(
                        form_params[field]["placeholder"]
                    );
                    txt_field.id = `${prefix}-${field}`;
                    txt_field.classList.add("new-value");
                    td.appendChild(txt_field);
                    break;
                default:
                    break;
            }
        } else {
            if (element) {
                td.innerText = element[field];
            }
        }

        row.appendChild(td);
    }
}

async function update_table(request = null) {
    // let response = await fetch(get_values_url, {
    let response = await fetch(
        Flask.url_for("tables.get_values", { table_name: table_name })
    );

    if (response.ok) {
        let json = await response.json();

        let tbody = document.getElementById("tbody");
        tbody.innerText = "";
        for (let element of json) {
            let row = document.createElement("tr");
            row.id = `row-${element[fields[0]]}`;

            let td = document.createElement("td");

            let btn = document.createElement("button");
            btn.classList.add("btn", "btn-primary");
            btn.innerText = "Изменить";
            btn.onclick = () => {
                prepare_update(element[fields[0]], element);
            };
            td.appendChild(btn);

            row.appendChild(td);
            for (let field of fields) {
                td = document.createElement("td");
                td.innerText =
                    element[field] !== null ? element[field] : "Пусто";
                row.appendChild(td);
            }
            td = document.createElement("td");
            btn = document.createElement("button");
            btn.classList.add("btn", "btn-danger");
            btn.innerText = "Удалить";
            btn.onclick = () => {
                delete_by_id(element[fields[0]]);
            };
            td.appendChild(btn);
            row.appendChild(td);

            tbody.appendChild(row);
        }
        let row = document.createElement("tr");
        let td = document.createElement("td");

        row.appendChild(td);

        add_form(row);

        td = document.createElement("td");

        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-success");
        btn.innerText = "Добавить";
        btn.onclick = insert;
        td.appendChild(btn);

        row.appendChild(td);
        tbody.appendChild(row);
    }
}

function prepare_update(id, element) {
    let row = document.getElementById(`row-${id}`);
    row.innerHTML = "";
    let td = document.createElement("td");

    let btn = document.createElement("button");
    btn.classList.add("btn", "btn-danger");
    btn.innerText = "Назад";
    btn.onclick = () => {
        cancel_update(id, element);
    };
    td.appendChild(btn);
    row.appendChild(td);

    add_form(row, id, element);

    td = document.createElement("td");

    btn = document.createElement("button");
    btn.classList.add("btn", "btn-success");
    btn.innerText = "Отправить";
    btn.onclick = () => {
        update(id)
    };
    td.appendChild(btn);

    row.appendChild(td);
}

function cancel_update(id, element) {
    let row = document.getElementById(`row-${id}`);
    row.innerText = "";

    let td = document.createElement("td");

    let btn = document.createElement("button");
    btn.classList.add("btn", "btn-primary");
    btn.innerText = "Изменить";
    btn.onclick = () => {
        prepare_update(element[fields[0]], element);
    };
    td.appendChild(btn);

    row.appendChild(td);
    for (let field of fields) {
        td = document.createElement("td");
        td.innerText = element[field] !== null ? element[field] : "Пусто";
        row.appendChild(td);
    }
    td = document.createElement("td");
    row.appendChild(td);
}

async function insert() {
    let data = {
        table: table_name,
    };
    for (let field in forms) {
        data[field] = document.getElementById(`new-${field}`).value;
    }
    console.log(data);

    let response = await fetch(Flask.url_for("tables.insert_value"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    update_table();
}

async function update(id) {
    let data = {
        table: table_name,
    };

    data[`${table_name}_id`] = id;

    for (let field in forms) {
        console.log(`${id}-${field}`);
        data[field] = document.getElementById(`${id}-${field}`).value;
    }
    console.log(data);

    let response = await fetch(Flask.url_for("tables.update_value"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    update_table();
}

async function delete_by_id(id) {
    let data = {
        table: table_name,
        id: id,
    };

    console.log(data);

    let response = await fetch(Flask.url_for("tables.delete_by_id"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    update_table();
}



create_table();
