"use strict";

function message(message) {
    let messages = document.getElementById("messages");
    messages.innerHTML = "";

    let message_card = document.createElement("div");
    message_card.className =
        "alert alert-danger alert-dismissible fade show col-12 col-md-8 mx-auto my-3";

    let btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn-close";
    btn.setAttribute("data-bs-dismiss", "alert");

    btn.ariaLabel = "Close";
    message_card.appendChild(btn);

    let strong = document.createElement("strong");
    strong.id = "message";
    strong.innerHTML = message;
    message_card.appendChild(strong);

    messages.appendChild(message_card);
}

const select_dct = {
    owner_name: "owner_id",
    city_name: "city_id",
    item_name: "item_id",
};

async function selector(table, field) {
    let select = document.createElement("select");
    select.className = "form-select";
    let response = await fetch(
        Flask.url_for("tables.get_values", { table_name: table })
    );

    if (response.ok) {
        let json = await response.json();

        for (let element in json) {
            let option = document.createElement("option");
            option.value = json[element][`${table}_id`];
            option.innerText = `${json[element][field]} - ${option.value}`;
            select.appendChild(option);
        }

        return select;
    } else {
        return null;
    }
}

function text_field(placeholder = "") {
    let text = document.createElement("input");
    text.className = "form-control";
    text.placeholder = placeholder;

    return text;
}

function number(placeholder = 0) {
    let text = document.createElement("input");
    text.type = "number";
    text.className = "form-control";
    text.placeholder = placeholder;

    return text;
}

function phone_number(placeholder = "80000000000") {
    let text = document.createElement("input");
    text.type = "tel";
    text.className = "form-control";
    text.placeholder = placeholder;

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

async function add_form(row, prefix = "new", element = null) {
    for (let field of fields) {
        let td = document.createElement("td");
        if (field in forms) {
            if (forms[field] === "text") {
                let txt_field = text_field(form_params[field]["placeholder"]);
                txt_field.id = `${prefix}-${field}`;
                txt_field.classList.add("new-value");
                td.appendChild(txt_field);
            } else if (forms[field] === "select") {
                let select = null;
                if (field === "owner_name") {
                    select = await selector("owner", field);
                    select.id = `${prefix}-${field}`;
                } else if (field === "storage_id") {
                    select = await selector("storage", field);
                    select.id = `${prefix}-${field}`;
                } else if (field === "item_name") {
                    select = await selector("item", field);
                    select.id = `${prefix}-${field}`;
                } else if (field === "city_name") {
                    select = await selector("city", field);
                }
                select.id = `${prefix}-${field}`;
                td.appendChild(select);
            } else if (forms[field] === "number") {
                let num = number(element ? element["area"] : 0);
                num.id = `${prefix}-${field}`;
                td.appendChild(num);
            } else if (forms[field] === "phone") {
                let tel = phone_number(
                    element ? element["phone_number"] : "80000000000"
                );
                tel.id = `${prefix}-${field}`;
                td.appendChild(tel);
            }
        } else {
            if (element) {
                td.innerText = element[field];
            }
        }

        row.appendChild(td);
    }
}

async function update_table(search_request = null) {
    // let response = await fetch(get_values_url, {
    console.log(search_request);
    let response = null;
    if (search_request) {
        let strict = document.getElementById("strictSearch").value;
        console.log(strict);
        response = await fetch(
            Flask.url_for("tables.search_values", { table_name: table_name }) +
                `?request=${search_request}&strict=${strict}`
        );
    } else {
        response = await fetch(
            Flask.url_for("tables.get_values", { table_name: table_name })
        );
    }

    if (response.ok) {
        let json = await response.json();

        let tbody = document.getElementById("tbody");
        tbody.innerText = "";

        let row = document.createElement("tr");
        let td = document.createElement("td");

        row.appendChild(td);

        await add_form(row);

        td = document.createElement("td");

        let btn = document.createElement("button");
        btn.classList.add("btn", "btn-success");
        btn.innerText = "Добавить";
        btn.onclick = insert;
        td.appendChild(btn);

        row.appendChild(td);
        tbody.appendChild(row);
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
    }
}

async function prepare_update(id, element) {
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

    await add_form(row, id, element);

    td = document.createElement("td");

    btn = document.createElement("button");
    btn.classList.add("btn", "btn-success");
    btn.innerText = "Отправить";
    btn.onclick = () => {
        update(id);
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
        if (forms[field] === "select") {
            data[select_dct[field]] = document.getElementById(
                `new-${field}`
            ).value;
        }
        data[field] = document.getElementById(`new-${field}`).value;
    }

    let response = await fetch(Flask.url_for("tables.insert_value"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    let json = await response.json();
    console.log(json);
    if ("error" in json) {
        message(json["error"]);
    }

    update_table();
}

async function update(id) {
    let data = {
        table: table_name,
    };

    data[`${table_name}_id`] = id;

    for (let field in forms) {
        if (forms[field] === "select") {
            data[field] = document.getElementById(`${id}-${field}`).value;
        }
    }

    let response = await fetch(Flask.url_for("tables.update_value"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    let json = await response.json();
    console.log(json);
    if ("error" in json) {
        message(json["error"]);
    }

    update_table();
}

async function delete_by_id(id) {
    let data = {
        table: table_name,
        id: id,
    };

    let response = await fetch(Flask.url_for("tables.delete_by_id"), {
        method: "POST",
        body: JSON.stringify(data),
    });

    let json = await response.json();
    console.log(json);
    if ("error" in json) {
        message(json["error"]);
    }

    update_table();
}

async function delete_by_index() {
    let data = {
        table_name: table_name,
        index: document.getElementById("search").value,
    };

    console.log(
        Flask.url_for("tables.delete_by_index", { table_name: table_name })
    );
    let response = await fetch(
        Flask.url_for("tables.delete_by_index", { table_name: table_name }),
        {
            method: "POST",
            body: JSON.stringify(data),
        }
    );

    let json = await response.json();
    console.log(json);
    if ("error" in json) {
        message(json["error"]);
    }

    update_table();
}

async function clear_table() {
    console.log("1");
    let response = await fetch(
        Flask.url_for("tables.table_clear", {
            table_name: table_name,
        })
    );

    let json = await response.json();
    console.log(json);
    if ("error" in json) {
        message(json["error"]);
    }

    update_table();
}

create_table();

let alertList = document.querySelectorAll(".alert");
alertList.forEach(function (alert) {
    new bootstrap.Alert(alert);
});
