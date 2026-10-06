const API_BASE = "http://127.0.0.1:5000/api";


// =========================================================
// GENERAL API REQUEST
// =========================================================

async function apiRequest(
    endpoint,
    options = {}
) {

    const config = {

        ...options,

        headers: {

            "Content-Type":
                "application/json",

            ...(options.headers || {})

        },

        credentials: "include"

    };


    const response = await fetch(
        API_BASE + endpoint,
        config
    );


    let data;

    try {

        data = await response.json();

    } catch {

        data = {
            success: false,
            message: "Invalid server response."
        };

    }


    if (!response.ok) {

        throw new Error(
            data.message ||
            "Something went wrong."
        );

    }


    return data;
}


// =========================================================
// LOGIN
// =========================================================

async function loginUser(
    email,
    password
) {

    return apiRequest(
        "/auth/login",
        {
            method: "POST",

            body: JSON.stringify({

                email,
                password

            })
        }
    );
}


// =========================================================
// SIGNUP
// =========================================================

async function signupUser(
    name,
    email,
    password
) {

    return apiRequest(
        "/auth/signup",
        {
            method: "POST",

            body: JSON.stringify({

                name,
                email,
                password

            })
        }
    );
}


// =========================================================
// LOGOUT
// =========================================================

async function logoutUser() {

    return apiRequest(
        "/auth/logout",
        {
            method: "POST"
        }
    );
}


// =========================================================
// CURRENT USER
// =========================================================

async function getCurrentUser() {

    return apiRequest(
        "/auth/me"
    );
}


// =========================================================
// DASHBOARD / HISTORY
// =========================================================
async function getHistory() {
    return apiRequest("/history");
}




// =========================================================
// AGRICULTURE ANALYSIS
// =========================================================

async function runAgricultureAnalysis(
    data
) {

    return apiRequest(
        "/prediction/agriculture",
        {
            method: "POST",

            body: JSON.stringify(data)
        }
    );
}


// =========================================================
// SINGLE ANALYSIS
// =========================================================

async function getAnalysis(
    id
) {

    return apiRequest(
        `/history/${id}`
    );
}


// =========================================================
// DELETE ANALYSIS
// =========================================================

async function deleteAnalysis(
    id
) {

    return apiRequest(
        `/history/${id}`,
        {
            method: "DELETE"
        }
    );
}