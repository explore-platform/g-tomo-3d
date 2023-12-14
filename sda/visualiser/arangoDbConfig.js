#!/usr/bin/env node

const SDA_ENV = process.env.SDA_ENV;
const isSDA = SDA_ENV !== undefined && process.env.SDA_ENV !== "no_env";

var arangoConfig = {
    url: `http://${isSDA ? `arango_${SDA_ENV.toLowerCase()}` : 'localhost'}:8529/`,
    dbName: "visualizer",
    annotations: "annotations",
    username: "user-name",
    password: "my-pwd",
    useDB: true
}

module.exports = arangoConfig;