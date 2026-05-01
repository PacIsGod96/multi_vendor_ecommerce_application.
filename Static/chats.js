const { act } = require("react");

console.log("JS LOADED")
document.addEventListener("DOMContentLoaded", () => {
    const chats = document.querySelectorAll(".chat_item");
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button")

    if(!chats.length || !chatMessages || !input || !sendBtn) return;

    const vendorId = window.currentUserId;
    let activeUserId = null

    async function loadChat(userId) {
        const res = await fetch(`/get_chat?user1=${vendorId}&user2=${userId}`)
        const data = await res.json();

        chatMessages.innerHTML = "";

        data.forEach(msg => {
            const div = document.createElement("div");
            div.classList.add("message");

            if (msg.sender_id === vendorId) {
                div.classList.add("vendor");
            } else {
                div.classList.add("customer");
            }

            div.textContent = msg.text;
            chatMessages.appendChild(div);
        });

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chats.forEach(chat => {
        chat.addEventListener("click", () => {
            activeUserId = chat.dataset.userid;

            chats.forEach(c => c.classList.remove("active"));
            chat.classList.add("active");

            loadChat(activeUserId);
        });
    });

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if (!text || !activeUserId) return;

        await fetch("/send_chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender_id: vendorId,
                receiver_id: activeUserId,
                text: text
            })
        });

        input.value = ""
        loadChat(activeUserId)
    });
});