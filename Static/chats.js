
console.log("JS LOADED")
document.addEventListener("DOMContentLoaded", () => {
    const chats = document.querySelectorAll(".chat_item");
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button")

    if(!chats.length || !chatMessages || !input || !sendBtn) return;

    const currentUserId = window.currentUserId;
    let chatPartnerId = null

    async function loadChat(userId) {
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
        loadChat(chatPartnerId)
    });
});