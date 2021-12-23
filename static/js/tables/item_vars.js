"use strict";

const table_name = "item";
const fields = ["item_id", "item_name", "owner_name", "area"];
const fields_names = ["ID", "Название", "Владелец", "Площадь"];

const forms = {
    item_name: "text",
    owner_name: "select",
    area: "number",
};

const form_params = {
    item_name: {
        placeholder: "Введите предмет",
    },
};