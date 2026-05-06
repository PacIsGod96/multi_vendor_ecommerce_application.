console.log("JS LOADED")

let chatPartnerId = null;
let currentUserId = null;
let chatMessages = null;
let input = null;
let sendBtn = null;

function renderMessages(messages) {
    if (!chatMessages) return;

    chatMessages.innerHTML = "";

    messages.forEach(msg => {
        const div = document.createElement("div");
        div.classList.add("message");

        if (Number(msg.sender_id) === Number(currentUserId)) {
            div.classList.add("vendor");
        } else {
            div.classList.add("customer")
        }

        div.textContent = msg.text;
        chatMessages.appendChild(div);
    });

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function vendorChat(el) {
    chatPartnerId = el.dataset.userid;

    console.log("chat opened with:", chatPartnerId)

    const chatBox = document.getElementById("vendorChat");
    chatBox.style.display = "block"

    const nameBox = document.getElementById("chatVendorName");
    if (nameBox) {
        nameBox.textContent = el.dataset.vendorname || "vendor"
    }

    loadMessages();
}

function closeChat() {
    document.getElementById("vendorChat").style.display = "none"

    chatPartnerId = null;

    if (chatMessages) {
        chatMessages.innerHTML = "";
    }
}

async function loadMessages() {
        if (!chatPartnerId || !currentUserId) return;
        if(!chatMessages) return;

        const res = await fetch(
            `/get_chat?user1=${currentUserId}&user2=${chatPartnerId}`
        );

        const data = await res.json();
        renderMessages(data);
}

document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button");

    if (!chatMessages || !input || !sendBtn) return;

    currentUserId = window.currentUserId;

    sendBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if (!text || !chatPartnerId) return;

        const div = document.createElement("div");
        div.classList.add("message", "vendor");
        div.textContent = text;

        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        input.value = "";

        await fetch("/send_chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: chatPartnerId,
                text: text
            })
        });

        loadMessages();
    });
});
