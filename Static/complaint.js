document.addEventListener("DOMContentLoaded", () => {
    const complaints = document.querySelectorAll(".complaint_item");
    const placeholder = document.querySelector(".response_placeholder");
    const responseContent = document.querySelector(".response_content");
    const responseMessages = document.querySelector(".response_messages");
    const input = document.querySelector(".response_input_bar input");
    const sendBtn = document.querySelector(".response_input_bar button");
    const responseBox = document.querySelector(".admin_complaint_response");
    const filter = document.getElementById("complaintTypes")

    let activeUser = null;

    if(!complaints.length || !placeholder || !responseContent || !responseMessages || !input || !sendBtn) return;

    responseContent.classList.add("admin_hidden");
    placeholder.classList.remove("admin_hidden");
    responseBox.classList.remove("active");

    const messages = {}

    complaints.forEach(item => {
        item.addEventListener("click", () => {
            activeUser = item.textContent.trim();

            complaints.forEach(c => c.classList.remove("active"));
            item.classList.add("active");

            placeholder.classList.add("admin_hidden");
            responseContent.classList.remove("admin_hidden");
            responseBox.classList.add("active");

            responseMessages.innerHTML = "";

            if(!messages[activeUser]) {
                messages[activeUser] = [];
            }

            messages[activeUser].forEach(message => {
                const msg = document.createElement("div");

                msg.classList.add("responses");

                if(message.sender === "admin") {
                    msg.classList.add("vendor");
                } else {
                    msg.classList.add("customer");
                }

                msg.textContent = message.text;

                responseMessages.appendChild(msg);
            });

            responseMessages.scrollTop = responseMessages.scrollHeight;

        });   
    });

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const text = input.value.trim();

        if(!text) return;

        if(!activeUser) {
            alert("Select a complaint first");
            return;
        }

        if(!messages[activeUser]) {
            messages[activeUser] = [];
        }

        messages[activeUser].push({
            text: text,
            sender: "admin"
        });

        const msg = document.createElement("div");
        msg.classList.add("responses", "vendor");
        msg.textContent = text;

        responseMessages.appendChild(msg);

        input.value = "";
        responseMessages.scrollTop = responseMessages.scrollHeight;
    });

    filter.addEventListener("change", () => {
        const selected = filter.value;

        complaints.forEach(item => {
            const type = item.dataset.type;

            if(selected === "all" || type === selected) {
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
        });
    });
});