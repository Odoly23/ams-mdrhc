// ===============================
// GLOBAL VARIABLE
// ===============================
let excelData = [];

// ===============================
// GET CSRF TOKEN FROM COOKIE
// ===============================
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// ===============================
// GENERIC POST FUNCTION
// ===============================
function postData(url, bodyData, isFormData = false) {

    let headers = {
        'X-CSRFToken': csrftoken
    };

    if (!isFormData) {
        headers['Content-Type'] = 'application/x-www-form-urlencoded';
    }

    return fetch(url, {
        method: "POST",
        headers: headers,
        body: bodyData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }
        return response.json();
    });
}

// ===============================
// UPLOAD EXCEL
// ===============================
function uploadExcel() {

    const fileInput = document.getElementById("excelFile");

    if (!fileInput.files.length) {
        alert("Please select an Excel file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    postData("/assets/Upload-excel/", formData, true)
        .then(data => {

            if (data.status === "success") {

                excelData = data.data;

                if (excelData.length === 0) {
                    alert("Excel file is empty.");
                    return;
                }

                renderTable(excelData);

            } else {
                alert("Failed to read Excel file.");
            }

        })
        .catch(error => {
            console.error(error);
            alert("Upload failed.");
        });
}

// ===============================
// RENDER PREVIEW TABLE
// ===============================
function renderTable(data) {

    const tableHead = document.querySelector("#previewTable thead");
    const tableBody = document.querySelector("#previewTable tbody");

    tableHead.innerHTML = "";
    tableBody.innerHTML = "";

    // HEADER
    let headerRow = "<tr>";
    headerRow += "<th><input type='checkbox' onclick='selectAll(this)'></th>";

    Object.keys(data[0]).forEach(key => {
        headerRow += "<th>" + key + "</th>";
    });

    headerRow += "</tr>";
    tableHead.innerHTML = headerRow;

    // BODY
    let bodyRows = "";

    data.forEach((row, index) => {

        bodyRows += "<tr>";
        bodyRows += "<td><input type='checkbox' class='row-check' value='" + index + "'></td>";

        Object.values(row).forEach(val => {
            bodyRows += "<td>" + (val ?? "") + "</td>";
        });

        bodyRows += "</tr>";
    });

    tableBody.innerHTML = bodyRows;
}

// ===============================
// SELECT ALL
// ===============================
function selectAll(source) {
    document.querySelectorAll('.row-check')
        .forEach(cb => cb.checked = source.checked);
}

// ===============================
// SAVE SELECTED ROWS
// ===============================
function saveSelected() {

    const selected = [];

    document.querySelectorAll('.row-check:checked')
        .forEach(cb => {
            selected.push(excelData[cb.value]);
        });

    if (selected.length === 0) {
        alert("Please select at least one row.");
        return;
    }

    postData(
        "/assets/Save-import/",
        "selected_rows=" + encodeURIComponent(JSON.stringify(selected))
    )
    .then(data => {

        if (data.status === "saved") {

            alert("Import Success!");

            // reload page after success
            location.reload();

        } else {
            alert("Failed to save data.");
        }

    })
    .catch(error => {
        console.error(error);
        alert("Save failed.");
    });
}