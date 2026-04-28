document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button");

    if (!chatMessages || !input || !sendBtn) return;

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        const msg = document.createElement("div");
        msg.classList.add("message", "vendor");
        msg.textContent = text;

        chatMessages.appendChild(msg);

        input.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
});

function vendorChat() {
    document.getElementById("vendorChat").style.display = "block";
}