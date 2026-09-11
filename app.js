function addMessage(text, type) {

    const messages =
        document.getElementById("messages");

    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble " + type;

    bubble.innerHTML =
        text.replace(/\n/g, "<br>");

    messages.appendChild(bubble);

    messages.scrollTop =
        messages.scrollHeight;
}


function ask(text) {

    document
        .getElementById("msg")
        .value = text;

    send();
}


async function send() {

    const input =
        document.getElementById("msg");

    const text =
        input.value.trim();


    if (!text) {
        return;
    }


    addMessage(
        text,
        "user"
    );


    input.value = "";


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: text
                    })
                }
            );


        const data =
            await response.json();


        addMessage(
            data.reply,
            "bot"
        );


        if (data.service) {

            const service =
                data.service;


            addMessage(

                `
                <b>${service.name}</b>

                <br><br>

                ${service.desc}

                <br><br>

                <b>Suggested Path:</b>

                <br>

                1. Check eligibility

                <br>

                2. Prepare documents

                <br>

                3. Use the official government portal

                <br>

                4. Track your application

                <br><br>

                <button
                    onclick='saveService("${service.name}")'
                    style="height:36px">

                    📌 Save Service

                </button>
                `,

                "bot"
            );
        }

    }

    catch (error) {

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    }

}


async function saveService(service) {

    const response =
        await fetch(
            "/api/save-application",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    service: service
                })
            }
        );


    if (response.ok) {

        addMessage(
            "✅ Service saved to My Applications.",
            "bot"
        );

    }

    else {

        addMessage(
            "Please log in to save this service.",
            "bot"
        );

    }

}