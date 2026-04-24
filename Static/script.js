const loginform = document.getElementById('login_form');

loginform.addEventListener('submit', () => {
    setTimeout(() => {
        loginform.reset()
    }, 50)
});

function handlesSignUpSubmit(event) {
    setTimeout(() => {
        const inputs = document.querySelectorAll('#signupForm input')
        
        inputs.forEach(input => input.value = "");

        document.getElementById("register_role").value = "user";

        showLogin();
    }, 100)

    return true;
}

function showRegister() {
    console.log("signup clicked")
    document.getElementById("panelContainer").classList.add("show-signup")
}

function showLogin() {
    console.log("login clicked")
    document.getElementById("panelContainer").classList.remove("show-signup")
}

function toggleEdit(id) {
    const input = document.getElementById(id);

    if(input.hasAttribute("readonly")) {
        input.removeAttribute("readonly");
        input.focus();
    }else{
        input.setAttribute("readonly", true)
    }
}

