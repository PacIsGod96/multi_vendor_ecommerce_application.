
console.log("JS LOADED")

let currentUserId = null;
let chatPartnerId = null;
let chatMessages = null;
let input = null;
let sendBtn = null;

console.log("currentUserId:", currentUserId);
console.log("chatPartnerId:", chatPartnerId);

async function loadInbox() {
    const res = await fetch("/get_inbox");
    const data = await res.json()
    const inbox = document.getElementById("inboxList")

    inbox.innerHTML = "";

    data.forEach(user => {
        const div = document.createElement("div");
        div.classList.add("chat_item");
        div.dataset.userid = user.account_id;
        div.textContent = user.username;

        div.addEventListener("click", () => {
            chatPartnerId = user.account_id;

            document.querySelectorAll(".chat_item").forEach(c => c.classList.remove("active"));
            div.classList.add("active");

            document.getElementById("chatContent").classList.remove("hidden");
            document.getElementById("chatPlaceholder").style.display = "none"

            loadChat(chatPartnerId);
        });

        inbox.appendChild(div);
    });
}

async function loadChat(userId) {
    const res = await fetch(`/get_chat?user1=${currentUserId}&user2=${userId}`);
    const data = await res.json();

    chatMessages.innerHTML = "";

    data.forEach(msg => {
        console.log("RENDERING MSG:", msg)
        const div = document.createElement("div");
        div.classList.add("message");

        const sender = Number(msg.sender_id);

        if (msg.sender_id === currentUserId) {
            div.classList.add("vendor");
        } else {
            div.classList.add("customer")
        }

        div.textContent = msg.text;
        chatMessages.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", () => {

    const chatData = document.getElementById("chatData");
    const chatContent = document.getElementById("chatContent")
    chatMessages = document.querySelector(".chat_messages");
    input = document.querySelector(".chat_input_bar input");
    sendBtn = document.querySelector(".chat_input_bar button")

    if(!chatMessages || !input || !sendBtn || !chatData) return;

    currentUserId = Number(chatData.dataset.userId);

    if(isNaN(currentUserId)) {
        console.log("currentUserId is invalid:", chatData.dataset.userId)
    }

    loadInbox();


    sendBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if (!text || !chatPartnerId) return;

        console.log("SENDING:", {
            sender_id: currentUserId,
            receiver_id: chatPartnerId,
            text: text
        });

        const div = document.createElement("div");
        div.classList.add("message", "vendor");
        div.textContent = text;
        chatMessages.appendChild(div)

        input.value = "";

        await fetch("/send_chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: chatPartnerId,
                text: text
            })
        });

        input.value = ""
        await loadChat(chatPartnerId);
    });
});