// ==========================================
// TRUSTAI AUTHENTICATION
// ==========================================


// ---------- SIGN UP ----------

function signupUser() {

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value;

    if (name === "" || email === "" || password === "") {
        alert("Please fill all details.");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return;
    }

    const user = {
        name: name,
        email: email,
        password: password
    };

    localStorage.setItem("trustai_user", JSON.stringify(user));

    alert("Account created successfully!");

    window.location.href = "login.html";
}


// ---------- LOGIN ----------

function loginUser() {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please enter email and password.");
        return;
    }

    const savedUser = localStorage.getItem("trustai_user");

    if (!savedUser) {
        alert("No account found. Please create an account first.");
        return;
    }

    const user = JSON.parse(savedUser);

    if (
        user.email === email &&
        user.password === password
    ) {

        // IMPORTANT:
        // This stays saved even when the user changes pages.
        localStorage.setItem("trustai_logged_in", "true");

        // Also save current user
        localStorage.setItem("trustai_current_user", JSON.stringify(user));

        window.location.href = "dashboard.html";

    } else {

        alert("Invalid email or password.");

    }
}


// ---------- CHECK LOGIN ----------

function checkLogin() {

    const loggedIn = localStorage.getItem("trustai_logged_in");

    if (loggedIn !== "true") {
        window.location.href = "login.html";
        return false;
    }

    return true;
}


// ---------- LOGOUT ----------

function logout() {

    localStorage.removeItem("trustai_logged_in");
    localStorage.removeItem("trustai_current_user");

    window.location.href = "login.html";
}


// ---------- GET CURRENT USER ----------

function getCurrentUser() {

    const user = localStorage.getItem("trustai_current_user");

    if (!user) {
        return null;
    }

    return JSON.parse(user);
}


// ---------- SHOW USER NAME ----------

function showUserName() {

    const user = getCurrentUser();

    if (!user) return;

    const elements = document.querySelectorAll(".user-name");

    elements.forEach(element => {
        element.textContent = user.name;
    });
}


// ---------- AUTO CHECK ----------

document.addEventListener("DOMContentLoaded", function () {

    showUserName();

});