// ==========================
// AI PDF Chatbot Pro
// ==========================

const uploadBtn = document.getElementById("uploadBtn");
const askBtn = document.getElementById("askBtn");
const clearBtn = document.getElementById("clearChat");

const pdfFile = document.getElementById("pdfFile");
const selectedFile = document.getElementById("selectedFile");
const fileList = document.getElementById("fileList");

const questionBox = document.getElementById("question");
const chatArea = document.getElementById("chatArea");

// ---------------------------
// Show Selected File Name
// ---------------------------

pdfFile.addEventListener("change", () => {

    if (pdfFile.files.length > 0) {

        selectedFile.innerHTML = pdfFile.files[0].name;

    } else {

        selectedFile.innerHTML = "No PDF Selected";

    }

});

// ---------------------------
// Upload PDF
// ---------------------------

uploadBtn.addEventListener("click", async () => {

    if (pdfFile.files.length === 0) {

        alert("Please select a PDF first.");

        return;

    }

    const formData = new FormData();

    formData.append("pdf", pdfFile.files[0]);

    uploadBtn.innerHTML = "Uploading...";

    uploadBtn.disabled = true;

    try {

        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        uploadBtn.innerHTML = "📄 Upload PDF";

        uploadBtn.disabled = false;

        if (response.ok) {

            fileList.innerHTML =
                `<li>📄 ${pdfFile.files[0].name}</li>`;

            addBotMessage("✅ PDF uploaded successfully! Ask me anything about it.");

        } else {

            addBotMessage("❌ " + data.message);

        }

    } catch (err) {

        uploadBtn.innerHTML = "📄 Upload PDF";

        uploadBtn.disabled = false;

        addBotMessage("❌ Upload failed.");

        console.error(err);

    }

});

// ---------------------------
// Ask AI
// ---------------------------

askBtn.addEventListener("click", askQuestion);

questionBox.addEventListener("keydown", function(e){

    if(e.key==="Enter" && !e.shiftKey){

        e.preventDefault();

        askQuestion();

    }

});

async function askQuestion(){

    const question = questionBox.value.trim();

    if(question===""){

        alert("Enter a question.");

        return;

    }

    addUserMessage(question);

    questionBox.value="";

    const typing = document.createElement("div");

    typing.className="bot-message";

    typing.id="typing";

    typing.innerHTML="🤖 Thinking...";

    chatArea.appendChild(typing);

    scrollChat();

    try{

        const response = await fetch("/ask",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                question:question

            })

        });

        const data = await response.json();

        document.getElementById("typing").remove();

        addBotMessage(data.answer);

    }

    catch(err){

        document.getElementById("typing").remove();

        addBotMessage("❌ Unable to connect to server.");

    }

}

// ---------------------------
// Messages
// ---------------------------

function addUserMessage(text){

    const div=document.createElement("div");

    div.className="user-message";

    div.innerHTML=text;

    chatArea.appendChild(div);

    scrollChat();

}

function addBotMessage(text){

    const div=document.createElement("div");

    div.className="bot-message";

    div.innerHTML=text;

    chatArea.appendChild(div);

    scrollChat();

}

// ---------------------------
// Scroll
// ---------------------------

function scrollChat(){

    chatArea.scrollTop=chatArea.scrollHeight;

}

// ---------------------------
// Clear Chat
// ---------------------------

clearBtn.addEventListener("click",()=>{

    chatArea.innerHTML=`
        <div class="bot-message">
            👋 Chat cleared. Upload a PDF and ask a new question.
        </div>
    `;

});