
console.log("JS LOADED")

let currentUserId = null;
let chatPartnerId = null;
let chat_messages = null;
let input = null;
let sendBtn = null;

document.addEventListener("DOMContentLoaded", () => {
    const chats = document.querySelectorAll(".chat_item");
    const chatData = document.getElementById("chatData");
    const chatContent = document.getElementById("chatContent")
    chatMessages = document.querySelector(".chat_messages");
    input = document.querySelector(".chat_input_bar input");
    sendBtn = document.querySelector(".chat_input_bar button")

    if(!chatMessages || !input || !sendBtn || !chatData) return;

    currentUserId = Number(chatData.dataset.userId);

    async function loadChat(userId) {
        if (!userId) return;

        const res = await fetch(`/get_chat?user1=${currentUserId}&user2=${userId}`)
        const data = await res.json();

        chatMessages.innerHTML = "";

        data.forEach(msg => {
            const div = document.createElement("div");
            div.classList.add("message");

            if (Number(msg.sender_id) === Number(currentUserId)) {
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
            chatPartnerId = chat.dataset.userid;

            chats.forEach(c => c.classList.remove("active"));
            chat.classList.add("active");

            chatContent.classList.remove("hidden");
            document.getElementById("chatPlaceholder").style.display = "none";

            loadChat(chatPartnerId);
        });
    });

    sendBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if (!text || !chatPartnerId) return;

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
    });
});