$(document).ready(function() {
    let chatBoxCount = 1;

    $("#add-box").click(function() {
        if (chatBoxCount < 4) {
            chatBoxCount++;
            const newBox = createChatBox(chatBoxCount);
            $("#chat-boxes").append(newBox);
        }
        adjustChatBoxLayout();
    });

    $("#remove-box").click(function() {
        if (chatBoxCount > 1) {
            $("#chat-boxes .chat-box").last().remove();
            chatBoxCount--;
        }
        adjustChatBoxLayout();
    });

    $("#refresh-box").click(function() {
        $(".output").text("Output will be shown here...");
        $(".chat-box").each(function(index) {
            $(this).replaceWith(createChatBox(index + 1));
        });
        adjustChatBoxLayout();
    });

    $("#stop-generation").click(function() {
        console.log("Stop generating response");
    });

    // Toggle overview button
    $("#overview").change(function() {
        if ($(this).is(":checked")) {
            $("#overview-output-cell").show();
            $("#overview-output-cell").html('<p>Overview:</p>');
        } else {
            $("#overview-output-cell").hide();
            $("#overview-output-cell").empty();
        }
    });

    // Add audience and role input bars
    $(document).on('click', '.add-input', function() {
        const type = $(this).data('type');
        const parentId = $(this).closest('.chat-box').attr('id');
        const inputField = `<input type="text" class="input-bar" id="${type}-${parentId}" placeholder="${type.charAt(0).toUpperCase() + type.slice(1)}" name="${type}-${parentId}">`;
        $(this).replaceWith(inputField);
        $(`#${type}-${parentId}`).fadeIn();
    });

    function createChatBox(index) {
        const boxId = `chat-box-${index}`;
        return `
            <div class="chat-box" id="${boxId}">
                <div class="input-group">
                    <div class="radio-group">
                        <label>Select AI Model:</label>
                        <label class="radio-label">
                            <input type="radio" id="gemini-${index}" name="model-${index}" value="gemini" checked>
                            <span class="radio-custom"></span>
                            <span class="radio-label-text">Google</span>
                        </label>
                        <label class="radio-label">
                            <input type="radio" id="gpt-${index}" name="model-${index}" value="gpt">
                            <span class="radio-custom"></span>
                            <span class="radio-label-text">OpenAI</span>
                        </label>
                        <label class="radio-label">
                            <input type="radio" id="groq-${index}" name="model-${index}" value="groq">
                            <span class="radio-custom"></span>
                            <span class="radio-label-text">Meta</span>
                        </label>
                    </div>
                    <div class="button-group">
                        <button type="button" class="add-input" data-type="audience">Add Audience</button>
                        <button type="button" class="add-input" data-type="role">Add Role</button>
                    </div>
                </div>
                <div class="output-cell">
                    <p class="output">Output:</p>
                </div>
            </div>
        `;
    }

    function adjustChatBoxLayout() {
        const chatBoxes = $(".chat-box");
        chatBoxes.each(function(index) {
            if (index % 2 === 0) {
                $(this).css("order", index);
            } else {
                $(this).css("order", index - 1);
            }
        });
    }
});
