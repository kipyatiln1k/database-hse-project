"use strict";

const table_name = "shelf";
const fields = ["shelf_id", "_number", "storage_id", "item_name", "area"];
const fields_names = ["ID", "Номер", "ID Склада", "Название предмета", "Площадь"];

const forms = {
    _number: "text",
    storage_id: "select",
    item_name: "select",
    area: "number",
};

const form_params = {
    _number: {
        placeholder: "Введите полку",
    },
};