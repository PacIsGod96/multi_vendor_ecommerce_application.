console.log("JS LOADED")
document.addEventListener("DOMContentLoaded", () => {
    const chats = document.querySelectorAll(".chat_item");
    const placeholder = document.getElementById("chatPlaceholder");
    const chatContent = document.getElementById("chatContent");
    const chatMessages = document.querySelector(".chat_messages");
    const input = document.querySelector(".chat_input_bar input");
    const sendBtn = document.querySelector(".chat_input_bar button")
    const chatBox = document.querySelector(".vendor_chat_box")

    let activeUser = null

    if(!chats.length || !placeholder || !chatContent || !chatMessages || !input || !sendBtn) return;

    chatContent.classList.add("hidden");
    placeholder.classList.remove("hidden")
    chatBox.classList.remove("active")

    const messages ={}

    chats.forEach(chat => {
        chat.addEventListener("click", () => {
            activeUser = chat.textContent.trim();

            chats.forEach(c => c.classList.remove("active"));
            chat.classList.add("active")

            placeholder.classList.add("hidden");
            chatContent.classList.remove("hidden");
            chatBox.classList.add("active")

            console.log("Active user:", activeUser);

            chatMessages.innerHTML = "";

            if(!messages[activeUser]) {
                messages[activeUser] = [];
            }

            messages[activeUser].forEach(message => {
                const msg = document.createElement("div");
                msg.classList.add("message", "customer");
                if(message.sender === "vendor" ) {
                    msg.classList.add("vendor");
                }else{
                    msg.classList.add("customer");
                }
                msg.textContent = message.text;
                chatMessages.appendChild(msg);
            });

            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    });

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if(!text) {
            return;
        }

        if(!activeUser) {
            alert("Select a user first");
            return;
        }

        if(!messages[activeUser]) {
            messages[activeUser] = [];
        }

        messages[activeUser].push({
            text: text,
            sender: "vendor"
        });

        const msg = document.createElement("div");
        msg.classList.add("message", "vendor");
        msg.textContent = text;

        chatMessages.appendChild(msg);

        input.value = "";

        chatMessages.scrollTop = chatMessages.scrollHeight;

        console.log(`Sent to ${activeUser}: ${text}`);
    })
})