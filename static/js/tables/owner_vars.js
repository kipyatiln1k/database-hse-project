"use strict";

const table_name = "owner";
const fields = ["owner_id", "owner_name", "phone_number"];
const fields_names = ["ID", "Имя", "Телефон"];

const forms = {
    owner_name: "text",
    phone_number: "phone",
};

const form_params = {
    owner_name: {
        placeholder: "Введите владельца",
    },
};