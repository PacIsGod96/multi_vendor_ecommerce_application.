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
    chatPartnerId = el.getAttribute("data-userid");

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
    chatMessages = document.querySelector(".chat_messages");
    input = document.querySelector(".chat_input_bar input");
    sendBtn = document.querySelector(".chat_input_bar button");

    if (!chatMessages || !input || !sendBtn) return;

    currentUserId = window.currentUserId;

    if (!currentUserId || currentUserId ==="null") {
        console.log("USER NOT LOGGED IN")
    }

    sendBtn.addEventListener("click", async (e) => {
        console.log("RAW CLICK FIRED");

        console.log("input:", input);
        console.log("chatMessages:", chatMessages);
        console.log("chatPartnerId:", chatPartnerId);
        console.log("currentUserId:", currentUserId);
        console.log("CHAT INIT RUNNING")
        console.log("SEND BUTTON", sendBtn)
        e.preventDefault();

        const text = input.value.trim();

        if (!text || !chatPartnerId || !currentUserId) return;

        const div = document.createElement("div");
        div.classList.add("message", "vendor");
        div.textContent = text;

        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        input.value = "";

        const res = await fetch("/send_chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: chatPartnerId,
                text: text
            })
        });

        const result = await res.json()
        console.log("send result:", result)

    });
})
