"use strict";

function create_table() {
    let head = document.getElementById("thead");
    let row = document.createElement("tr");

    for (let field_name of fields_names) {
        let th = document.createElement("th");
        th.innerText = field_name;
        th.classList.add("lead");
        row.appendChild(th);
    }

    head.appendChild(row);

    update_table();
}

async function update_table(request = null) {
    let response = await fetch(get_values_url, {
        method: "POST",
    });

    if (response.ok) {
        let json = await response.json();
        console.log(json);

        let tbody = document.getElementById("tbody");
        tbody.innerText = "";
        for (let element of json) {
            let row = document.createElement("tr");
            for (let field of fields) {
                let td = document.createElement("td");
                td.innerText = element[field] ? element[field] : 'Пусто';
                row.appendChild(td);
            }
            tbody.appendChild(row);
        }
    }
}

create_table();
