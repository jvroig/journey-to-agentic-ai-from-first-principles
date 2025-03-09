// Add event listeners to the tab buttons
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.nav-link');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('aria-controls');
            updateSidebar(tabId);
        });
    });

    console.log(`Loading event listeners for chat actions...`)
    document.getElementById(`send-button`).addEventListener('click', () => sendMessage());
    document.getElementById(`regenerate-button`).addEventListener('click', () => regenerateLastMessage());
    document.getElementById(`clear-chat-history`).addEventListener('click', () => clearChatHistory());
    document.getElementById(`save-chat`).addEventListener('click', () => saveChat());
    document.getElementById(`restore-chat`).addEventListener('click', () => document.getElementById(`file-input`).click());
    document.getElementById(`file-input`).addEventListener('change', (event) => restoreChat(event));
    document.getElementById(`chat-input`).addEventListener('keydown', function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            sendMessage();
            event.preventDefault();
        }
    });
});

let chat_context = [];
let currentMessageElement = null;
let currentTextElement = null;
let isFirstAssistantChunk = true;

function showTypingIndicator() {
    document.getElementById("typing-indicator").style.display = 'block'
    scrollToBottom()
}

function hideTypingIndicator(id) {
    document.getElementById("typing-indicator").style.display = 'none'
}

function escapeHTML(html) {
    return html
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
}

function sendMessage(regenerate = false) {
    let chatContext = [];
    let userInput = '';
    let sendButton = '';
    let typingIndicatorId = '';

    chatContext = chat_context;
    userInput = document.getElementById(`chat-input`);
    sendButton = document.getElementById(`send-button`);
    regenerateButton = document.getElementById(`regenerate-button`);
    clearChatButton = document.getElementById(`clear-chat-history`);
    typingIndicatorId = `typing-indicator`;
    chatInput = `chat-input`;

    // Get the message text from the input field
    var messageInput = document.getElementById(chatInput);
    var message = messageInput.value.trim();

    if (message !== "" || regenerate === true) {

        if (regenerate === false) {
            // Display the user's new message in the chat and add to context
            appendMessage("user", message);
        }

        // Clear the input field after sending the message
        messageInput.value = "";

        // Disable input and buttons
        userInput.disabled = true;
        sendButton.disabled = true;
        regenerateButton.disabled = true;
        clearChatButton.disabled = true;
        showTypingIndicator();

        // Use fetch to POST the message to the query endpoint API
        fetch('http://localhost:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: chatContext,
                temperature: 0.4,
                max_output_tokens: 1000,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            return readStream(reader, decoder);
        })
        .catch(error => {
            console.error('Error:', error);
            hideTypingIndicator(); // Hide typing indicator on error
            appendMessage('assistant', 'An error occurred while processing your request.');
        });

        function readStream(reader, decoder) {
            return reader.read().then(({ done, value }) => {
                if (done) {
                    hideTypingIndicator();
                    userInput.disabled = false;
                    sendButton.disabled = false;
                    regenerateButton.disabled = false;
                    clearChatButton.disabled = false;
                    isFirstAssistantChunk = true;
                    userInput.focus();
                    return;
                }
        
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n').filter(line => line.trim() !== '');
        
                for (const line of lines) {
                    try {
                        const data = JSON.parse(line);
                        
                        // Handle different message types
                        if (data.type === 'done') {
                            // Finalize the current message
                            appendMessage(data.role, '', 'done');
                            if (data.role === 'assistant') {
                                isFirstAssistantChunk = true;  // Reset for next assistant message
                            }
                        } else if (data.role === 'assistant') {
                            // Handle streaming assistant messages
                            let chunkType = isFirstAssistantChunk ? 'first_chunk' : 'chunk';
                            appendMessage('assistant', data.content, chunkType);
                            isFirstAssistantChunk = false;
                        } else if (data.role === 'tool_call' || data.role === 'user') {
                            // Handle non-streaming tool calls and user messages
                            // Force these to be new messages by resetting current elements
                            currentMessageElement = null;
                            currentTextElement = null;
                            appendMessage(data.role, data.content, data.type || 'regular');
                        }
                    } catch (error) {
                        console.error('Error parsing streamed message:', error, 'Chunk:', line);
                    }
                }
        
                return readStream(reader, decoder);
            })
        }
    }
}

function regenerateLastMessage() {
    let chatContext = [];
    let typingIndicatorId = '';

    chatContext = chat_context
    typingIndicatorId = `typing-indicator`;

    console.log(chatContext.length);
    if (chatContext.length < 2) {
        console.log("Not enough messages to regenerate");
        return;
    }

    // Remove the last bot message from the chat area
    const chatArea = document.getElementById(`chat-area`);
    const typingIndicator = document.getElementById(`typing-indicator`);
    
    // Find the last bot message (excluding the typing indicator)
    let lastBotMessage = null;
    for (let i = chatArea.children.length - 1; i >= 0; i--) {
        if (chatArea.children[i].classList.contains('assistant') && chatArea.children[i] !== typingIndicator) {
            lastBotMessage = chatArea.children[i];
            break;
        }
    }

    // Remove the last bot message if found
    if (lastBotMessage) {
        chatArea.removeChild(lastBotMessage);
    } else {
        console.log("No bot message found to regenerate");
        return;
    }

    // Remove the last bot message from the context
    chatContext.pop();

    sendMessage(true);
}

function appendMessage(sender, message, type = 'regular') {
    const chatArea = document.getElementById('chat-area');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // Create new message element for:
    // 1. First chunks of streaming messages
    // 2. Regular (non-streaming) messages
    // 3. Force new message for tool calls and user messages
    if (type === 'first_chunk' || 
        type === 'regular' || 
        (sender === 'tool_call' || sender === 'user')) {
        
        currentMessageElement = document.createElement('div');
        currentMessageElement.classList.add('chat-message', sender);
        
        // Add the appropriate title/icon based on sender
        if (sender === 'assistant') {
            const botTitle = document.createElement('div');
            botTitle.classList.add('bot-title');
            const botImage = document.createElement('i');
            botImage.classList = 'bot-logo bi bi-gear-wide-connected';
            botTitle.appendChild(botImage);
            currentMessageElement.appendChild(botTitle);
        } else if (sender === 'tool_call') {
            const botTitle = document.createElement('div');
            botTitle.classList.add('bot-title');
            const botImage = document.createElement('i');
            botImage.classList = 'bot-logo bi bi-tools';
            botTitle.appendChild(botImage);
            currentMessageElement.appendChild(botTitle);
        } else {
            const userTitle = document.createElement('div');
            userTitle.classList.add('user-title');
            const userImage = document.createElement('i');
            userImage.classList = 'user-logo bi bi-person-circle';
            userTitle.appendChild(userImage);
            currentMessageElement.appendChild(userTitle);
        }

        currentTextElement = document.createElement('div');
        currentMessageElement.appendChild(currentTextElement);
        chatArea.insertBefore(currentMessageElement, typingIndicator);
    }

    // Handle the message content
    if (type === 'chunk' || type === 'first_chunk') {
        // For streaming chunks, append to existing content
        let currentContent = escapeHTML(currentTextElement.innerHTML);
        let newContent = message.replace(/\n/g, '<br>');
        currentTextElement.innerHTML = currentContent + newContent;
    } else if (type === 'done') {
        // When streaming is complete, add to chat context and reset current elements
        if (currentTextElement) {
            chat_context.push({ 
                role: sender === 'assistant' ? 'assistant' : 'user', 
                content: currentTextElement.textContent 
            });
        }
        currentMessageElement = null;
        currentTextElement = null;
    } else {
        // For non-streaming messages (tool calls and regular messages)
        currentTextElement.innerHTML = escapeHTML(message.replace(/\n/g, '<br>'));
        chat_context.push({ 
            role: sender === 'assistant' ? 'assistant' : 'user', 
            content: message 
        });
        currentMessageElement = null;
        currentTextElement = null;
    }

    scrollToBottom();
}


function clearChatHistory() {
    if (confirm("Are you sure you want to clear the chat history? This action cannot be undone.")) {
        chatAreaId = `chat-area`;
        typingIndicatorId = `typing-indicator`; 
        const chatArea = document.getElementById(chatAreaId);
        const typingIndicator = document.getElementById(typingIndicatorId);

        console.log(typingIndicatorId)
        console.log(typingIndicator)

        if (!chatArea || !typingIndicator) {
            console.error('Chat area or typing indicator not found');
            return;
        }

        // Remove all child elements except the typing indicator
        Array.from(chatArea.children).forEach(child => {
            if (child !== typingIndicator) {
                chatArea.removeChild(child);
            }
        });

        // Ensure the typing indicator is the last child
        chatArea.appendChild(typingIndicator);

        //Clear the context for this tab
        chat_context = [];
    }
}

function saveChat() {
    const chatContext = chat_context;
    const yaml = jsyaml.dump(chatContext);
    const blob = new Blob([yaml], { type: 'text/yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat_${new Date().toISOString()}.yaml`;
    a.click();
    URL.revokeObjectURL(url);
}

function restoreChat(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const restoredChat = jsyaml.load(e.target.result);
                if (Array.isArray(restoredChat) && restoredChat.every(msg => msg.role && msg.content)) {
                    const chat_area = `chat-area`;
                    const typing_indicator = `typing-indicator`;

                    // Clear existing chat
                    clearChatHistory();
                    
                    // Restore messages
                    restoredChat.forEach(msg => {
                        console.log(msg.role)
                        console.log(msg.content)
                        console.log(chat_area)
                        console.log(typing_indicator)
                        appendMessage(msg.role, msg.content);
                    });

                    // Update context
                    chat_context = restoredChat;
                } else {
                    throw new Error('Invalid file format');
                }
            } catch (error) {
                console.error('Error parsing YAML:', error);
                appendMessage('assistant', 'Error restoring chat history. Please ensure you uploaded a valid file.');
            }
        };
        reader.readAsText(file);
    }
}

function scrollToBottom() {
    const chatArea = document.getElementById('chat-area');
    chatArea.scrollTo({
        top: chatArea.scrollHeight,
        behavior: 'smooth'
    });
}