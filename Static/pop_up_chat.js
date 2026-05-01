document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button");

    if (!chatMessages || !input || !sendBtn) return;

    const currentUserId = window.currentUserId;
    const vednotId = window.vendorId;

    function renderMessages() {
        chatMessages.innerHTML = "";

        messages.forEach(msg => {
            const div = document.createElement("div");
            div.classList.add("message");

            if (msg.sender_id === currentUserId) {
                div.classList.add("vendor");
            } else {
                div.classList.add("customer")
            }

            div.textContent = msg.text;
            chatMessages.appendChild(div);
        });

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function loadMessages() {
        const res = await fetch(`/get_chat?user1=${currentUserId}&user2=${vendorId}`)
        const data = await res.json();
        renderMessages(data);
    }

    sendBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        await fetch("/send_chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: vendorId,
                text: text
            })
        })

        input.value = "";
        loadMessages();
    });
    
    loadMessages();
});

function vendorChat() {
    document.getElementById("vendorChat").style.display = "block";
}