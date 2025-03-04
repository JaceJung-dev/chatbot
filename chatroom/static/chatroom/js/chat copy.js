// WebSocket 연결 설정
const chatroom_id = 1; // 실제 사용 시 chatroom_id를 동적으로 설정해야 함
const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chatroom/${chatroom_id}/`);

// WebSocket 연결 성공 시 실행
socket.onopen = function () {
    console.log("✅ WebSocket 연결 성공!");
};

// WebSocket 메시지 수신 시 실행
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const chatBox = document.querySelector(".frame7"); // 채팅 메시지 추가 위치

    // ✅ "답변을 생성 중입니다..." 표시 (최초 메시지)
    if (data.is_streaming && data.bot_message === "⌛ 답변을 생성 중입니다...") {
        chatBox.innerHTML += `
            <div class="frame8 bot-message">
                <div class="avatar3">
                    <img class="cpu" src="/static/chatroom/img/cpu0.svg" />
                </div>
                <div class="frame9">
                    <div class="frame10">
                        <div class="frame11">
                            <div class="frame12">
                                <div class="vermillion-gray">slothGPT</div>
                            </div>
                            <div class="_02-22-am">${getCurrentTime()}</div>
                        </div>
                        <div class="frame14">
                            <div id="bot-message" class="lorem-ipsum-dolor-sit-amet">⌛ 답변을 생성 중입니다...</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // ✅ 스트리밍 중이면 기존 메시지 업데이트
    if (data.is_streaming && data.bot_message !== "⌛ 답변을 생성 중입니다...") {
        let botMessageElement = document.getElementById("bot-message");
        if (botMessageElement) {
            botMessageElement.innerText = data.bot_message;
        }
    }

    // ✅ 스트리밍 종료 시 최종 응답 업데이트
    if (!data.is_streaming) {
        let botMessageElement = document.getElementById("bot-message");
        if (botMessageElement) {
            botMessageElement.innerText = data.bot_message;
            botMessageElement.removeAttribute("id");
        }
    }
};

// 메시지 전송 함수
function sendMessage() {
    const inputField = document.querySelector(".write-your-message-here");
    const message = inputField.innerText.trim();

    if (message === "") return; // 빈 메시지는 전송하지 않음

    // 채팅 UI에 사용자 메시지 추가
    const chatBox = document.querySelector(".frame7");
    chatBox.innerHTML += `
        <div class="frame8">
            <img class="avatar2" src="/static/chatroom/img/avatar1.png" />
            <div class="frame9">
                <div class="frame10">
                    <div class="frame11">
                        <div class="frame12">
                            <div class="vermillion-gray">You</div>
                        </div>
                        <div class="_02-22-am">${getCurrentTime()}</div>
                    </div>
                    <div class="frame13">
                        <div class="lorem-ipsum-dolor-sit-amet">${message}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // WebSocket을 통해 서버로 메시지 전송
    socket.send(JSON.stringify({ message: message }));

    // 입력 필드 초기화
    inputField.innerText = "";
}

// 현재 시간 반환 함수 (AM/PM 포맷)
function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12 || 12; // 12시간 형식으로 변환
    minutes = minutes < 10 ? "0" + minutes : minutes;
    return `${hours}:${minutes} ${ampm}`;
}

// 메시지 입력 시 엔터키 입력 감지하여 메시지 전송
document.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // 줄바꿈 방지
        sendMessage();
    }
});
