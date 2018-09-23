let http = require("http");

let options = {
    host: "developer.api.autodesk.com",
    path: "/oss/v1/buckets",
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer token"
    }
};