// WebSocket 연결 설정
const chatroom_id = 1; // 실제 사용 시 chatroom_id를 동적으로 설정해야 함
const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chatroom/${chatroom_id}/`);

// WebSocket 연결 성공 시 실행
socket.onopen = function () {
    console.log("✅ WebSocket 연결 성공!");
};

// WebSocket 연결 종료 시 재연결 시도
socket.onclose = function () {
    console.log("⚠️ WebSocket 연결이 종료되었습니다. 재연결을 시도합니다...");
    setTimeout(() => {
        location.reload(); // 페이지 새로고침으로 재연결 시도
    }, 2000);
};

// WebSocket 메시지 수신 시 실행
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const chatBox = document.getElementById("chat-box");

    if (data.is_streaming) {
        // 스트리밍이 진행 중이면 기존 메시지를 업데이트
        let botMessageElement = document.getElementById("bot-message");
        if (!botMessageElement) {
            botMessageElement = document.createElement("div");
            botMessageElement.id = "bot-message";
            botMessageElement.classList.add("message", "bot-message");
            chatBox.appendChild(botMessageElement);
        }
        botMessageElement.innerHTML= data.bot_message;
    } else {
        // 스트리밍이 끝나면 ID 제거하여 최종 메시지로 고정
        let botMessageElement = document.getElementById("bot-message");
        if (botMessageElement) {
            botMessageElement.innerHTML= data.bot_message;
            botMessageElement.removeAttribute("id");
        }
    }

    chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 최신 메시지로 이동
};

// 메시지 전송 함수
function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    
    // console.log("📩 sendMessage() 실행됨!"); // 실행 확인

    if (message === "") {
        console.log("⚠️ 빈 메시지는 전송되지 않습니다.");
        return; // 빈 메시지는 전송하지 않음
    }

    const chatBox = document.getElementById("chat-box");
    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user-message");
    userMessageElement.innerText = message;
    chatBox.appendChild(userMessageElement);

    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ message: message }));
        console.log("✅ WebSocket을 통해 메시지가 전송됨!");
    } else {
        console.log("❌ WebSocket이 열려있지 않음!");
    }

    inputField.value = ""; // 입력 필드 초기화
    chatBox.scrollTop = chatBox.scrollHeight;
    
}

// 수정된 키 입력 처리 함수 - keypress 이벤트 사용
function handleKeyPress(event) {
    console.log("⌨️ 키보드 입력 감지됨:", event.key);
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // 기본 Enter 동작(줄바꿈) 방지
        sendMessage();
    }
}

// HTML이 로드된 후 이벤트 리스너 등록
document.addEventListener("DOMContentLoaded", function () {
    // keydown 대신 keypress 이벤트 사용
    document.getElementById("user-input").addEventListener("keypress", handleKeyPress);
    
    // 전송 버튼이 있는 경우 클릭 이벤트 등록
    const sendButton = document.getElementById("send-button");
    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    }
});