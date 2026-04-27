let loginform = document.getElementById("login_form");

if (loginform) {
    loginform.addEventListener("submit", () => {
        setTimeout(() => {
            loginform.reset();
        }, 50);
    });
}

function handlesSignUpSubmit(event) {
    setTimeout(() => {
        const inputs = document.querySelectorAll('#signupForm input');
        inputs.forEach(input => input.value = "");

        document.getElementById("register_role").value = "user";
        showLogin();
    }, 100);

    return true;
}

function showRegister() {
    console.log("signup clicked");
    document.getElementById("panelContainer").classList.add("show-signup");
}

function showLogin() {
    console.log("login clicked");
    document.getElementById("panelContainer").classList.remove("show-signup");
}

function toggleEdit(id) {
    const input = document.getElementById(id);

    if (input.hasAttribute("readonly")) {
        input.removeAttribute("readonly");
        input.focus();
    } else {
        input.setAttribute("readonly", true);
    }
}

function showConfirm() {
    document.getElementById("cartPage").classList.add("hidden");
    document.getElementById("confirmOrderPage").classList.remove("hidden");
    fillConfirmSummary();
}

function showAdmin() {
    document.getElementById("confirmOrderPage").classList.add("hidden");
    document.getElementById("adminOrderQueue").classList.remove("hidden");
    fillAdminOrder();
}

function attachRemoveButtons() {
    document.querySelectorAll(".remove-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            this.parentElement.remove();
            updateTotal();
        });
    });
}

attachRemoveButtons();

function updateTotal() {
    let total = 0;

    document.querySelectorAll(".cart-price").forEach(p => {
        total += parseFloat(p.textContent.replace("$", ""));
    });

    document.getElementById("cartTotal").textContent = "Total: $" + total;
}

function fillConfirmSummary() {
    const items = document.querySelectorAll("#cartItems .cart-item");
    const summary = document.getElementById("confirmSummary");

    let html = "<h3>Order Summary</h3>";
    let total = 0;

    items.forEach(item => {
        const name = item.querySelector(".cart-name").textContent;
        const price = item.querySelector(".cart-price").textContent.replace("$", "");
        total += parseFloat(price);

        html += `<p>${name} — $${price}</p>`;
    });

    html += `<h3>Total: $${total}</h3>`;
    summary.innerHTML = html;
}

function fillAdminOrder() {
    const name = document.getElementById("confirmName").value;
    const email = document.getElementById("confirmEmail").value;
    const address = document.getElementById("confirmAddress").value;

    const items = document.querySelectorAll("#cartItems .cart-item");

    let total = 0;
    let itemsHTML = "";

    items.forEach(item => {
        const itemName = item.querySelector(".cart-name").textContent;
        const price = item.querySelector(".cart-price").textContent.replace("$", "");
        total += parseFloat(price);

        itemsHTML += `<p>- ${itemName}</p>`;
    });

    document.getElementById("adminOrderBox").innerHTML = `
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Address:</strong> ${address}</p>
        <p><strong>Total:</strong> $${total}</p>

        <h4>Items:</h4>
        ${itemsHTML}

        <button class="checkout-btn">Approve</button>
    `;
}

let draggedOrder = null;

function startDrag(event) {
    draggedOrder = event.target.closest(".order-item");
    if (!draggedOrder) return;

    draggedOrder.classList.add("dragging");
    event.dataTransfer.setData("text/plain", "dragging");
}

function endDrag(event) {
    if (draggedOrder) {
        draggedOrder.classList.remove("dragging");
    }
}

function allowDrop(event) {
    event.preventDefault();
}

function dropOrder(event) {
    event.preventDefault();

    if (!draggedOrder) return;

    const target = document.getElementById("confirmedOrders");

    if (target) {
        target.appendChild(draggedOrder);
    }

    draggedOrder = null;
}
