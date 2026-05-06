const loginform = document.getElementById('login_form');

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


function popUp(product) {

    const popup = document.getElementById("pop-up");
    popup.style.display = "block";

    // Basic info
    document.getElementById("popup-name").innerText = product.name;
    document.getElementById("popup-vendor").innerText = "By " + product.vendor;
    document.getElementById("popup-price").innerText = "$" + (product.price || "16.99");

    // 🔥 IMAGES CAROUSEL
    const imgContainer = document.getElementById("popup-images");
    imgContainer.innerHTML = "";

    if (product.images && product.images.length > 0) {
        product.images.forEach(img => {
            const image = document.createElement("img");
            image.src = "/static/" + img;
            imgContainer.appendChild(image);
        });
    }

    // 🔥 COLORS
    const colorSelect = document.getElementById("popup-color");
    colorSelect.innerHTML = "";

    if (product.colors) {
        product.colors.forEach(color => {
            let option = document.createElement("option");
            option.value = color;
            option.text = color;
            colorSelect.appendChild(option);
        });
    }

    // 🔥 SIZES
    const sizeSelect = document.getElementById("popup-size");
    sizeSelect.innerHTML = "";

    if (product.sizes) {
        product.sizes.forEach(size => {
            let option = document.createElement("option");
            option.value = size;
            option.text = size;
            sizeSelect.appendChild(option);
        });
    }
}

function closePopup() {
    document.getElementById("pop-up").style.display = "none";
}


function confirmAdd() {
    const productName = document.getElementById("popup-name").innerText;
    const color = document.getElementById("popup-color").value;
    const size = document.getElementById("popup-size").value;
    const qty = document.getElementById("popup-qty").value;

    console.log("ADD TO CART:", {
        productName,
        color,
        size,
        qty
    });

    closePopup();
}

function addProduct() {
    const addWindow = document.getElementById('addProduct');
    addWindow.style.display = 'block';
}

function confirmProduct() {
    const addWindow = document.getElementById('addProduct');
    addWindow.style.display = 'none';
}

function editProduct(product) {
    // 1. Show the edit modal window
    const editWindow = document.getElementById('editProduct');
    editWindow.style.display = 'block';

    // 2. Set only the hidden ID field (required so Flask knows which row to update)
    document.getElementById('edit_product_id').value = product.product_id;

    // 3. Reset form fields so they start completely blank (enabling partial updates)
    document.getElementById('edit_name').value = "";
    document.getElementById('edit_name').placeholder = `Current: ${product.name}`;
    
    document.getElementById('edit_price').value = "";
    document.getElementById('edit_price').placeholder = `Current: $${product.price}`;

    // 4. Uncheck all sizes so they don't overwrite current configurations by accident
    const possibleSizes = ['S', 'M', 'L', 'XL', 'XXL'];
    possibleSizes.forEach(size => {
        const checkbox = document.getElementById(`size_${size}`);
        if (checkbox) {
            checkbox.checked = false; 
        }
    });

    // 5. Clear old values in colors text inputs
    for (let i = 0; i < 3; i++) {
        const colorInput = document.getElementById(`edit_color_${i}`);
        if (colorInput) {
            colorInput.value = "";
            colorInput.placeholder = product.colors[i] ? `Current: ${product.colors[i]}` : "Add new color";
        }
    }

    // 6. Clear old values in image text inputs
    for (let i = 0; i < 3; i++) {
        const imageInput = document.getElementById(`edit_image_${i}`);
        if (imageInput) {
            imageInput.value = "";
            imageInput.placeholder = product.images[i] ? `Current: ${product.images[i]}` : "Add new image path";
        }
    }
}

function confirmEdit() {
    const editWindow = document.getElementById('editProduct');
    editWindow.style.display = 'none';
}

function deleteProduct() {
    const deleteWindow = document.getElementById('deleteProduct');
    deleteWindow.style.display = "block"
}

function confirmDelete() {
    const deleteWindow = document.getElementById('deleteProduct');
    deleteWindow.style.display = "none"
}

function exitDelete() {
    const deleteWindow = document.getElementById('deleteProduct');
    deleteWindow.style.display = "none"    
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

// rating
function showExplanation(rating) {
    const feedbackDiv = document.getElementById('extra-feedback');
    const label = document.getElementById('explanation-label');
    
    if (!feedbackDiv || !label) return;
    feedbackDiv.style.display = 'block';
    switch(rating) {
        case 5:
            label.innerText = "5 Shirts! What was the best part?";
            break;
        case 4:
            label.innerText = "Glad you liked it! Any small tips for us?";
            break;
        case 3:
            label.innerText = "What can we do to earn those last 2 shirts?";
            break;
        case 2:
            label.innerText = "We missed the mark. What exactly went wrong?";
            break;
        case 1:
            label.innerText = "We're sorry. Please tell us how we can fix this.";
            break;
        default:
            label.innerText = "Tell us more about your rating:";
    }
}
function toggleRatingSection() {
    const category = document.getElementById('category').value;
    const ratingArea = document.querySelector('.rating-area');
    const extraFeedback = document.getElementById('extra-feedback');

    if (category === 'Review') {
        ratingArea.style.display = 'block';
    } else {
        ratingArea.style.display = 'none';
        if(extraFeedback) extraFeedback.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', toggleRatingSection);

function toggleFormPanels() {
    const category = document.getElementById('category').value;
    
    // Hide all panels
    const panels = document.querySelectorAll('.dynamic-panel');
    panels.forEach(panel => panel.style.display = 'none');

    if (category === '') return;

    document.getElementById('panel-message').style.display = 'block';
    
    if (category === 'Review') {
        document.getElementById('panel-review').style.display = 'block';
    } else if (category === 'Complaint') {
        document.getElementById('panel-complaint').style.display = 'block';
    } else if (category === 'Refund') {
        document.getElementById('panel-refund').style.display = 'block';
    } else if (category === 'Warranty') {
        document.getElementById('panel-warranty').style.display = 'block';
    }
}

function showExplanation(rating) {
    const feedbackDiv = document.getElementById('extra-feedback');
    const label = document.getElementById('explanation-label');
    
    feedbackDiv.style.display = 'block';

    switch(rating) {
        case 5: label.innerText = "5 Shirts! What was the best part?"; break;
        case 4: label.innerText = "Glad you liked it! Any small tips?"; break;
        case 3: label.innerText = "How can we earn those last 2 shirts?"; break;
        case 2: label.innerText = "What exactly went wrong?"; break;
        case 1: label.innerText = "How can we fix this for you?"; break;
    }
}
document.addEventListener('DOMContentLoaded', toggleFormPanels);


function toggleFormPanels() {
    const category = document.getElementById('category').value;
    
    const panels = document.querySelectorAll('.dynamic-panel');
    panels.forEach(panel => panel.style.display = 'none');

    if (category === '') return;

    document.getElementById('panel-message').style.display = 'block';
    document.getElementById('panel-image').style.display = 'block';

    if (category === 'Review') {
        document.getElementById('panel-review').style.display = 'block';
    } else {

        document.getElementById('panel-order-info').style.display = 'block';
    }
}