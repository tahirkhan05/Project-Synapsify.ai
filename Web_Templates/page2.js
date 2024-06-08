$(document).ready(function() {
    // Variable to keep track of the number of chat boxes
    let chatBoxCount = 1;

    // Function to create a new chat box
    // Function to create a new chat box
function createChatBox(index) {
    const boxId = `chat-box-${index}`;
    return `
        <div class="chat-box" id="${boxId}">
            <div class="input-group">
                <div class="radio-group">
                    <label>Provider:</label>
                    <label class="radio-label">
                        <input type="radio" id="gemini-${index}" name="model-${index}" value="gemini">
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
                    <div class="model-select">
                    <select id="model-select-${index}" disabled>
                        <option value="">Select a model</option>
                    </select>
                </div>
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


    // Event listener for adding a new chat box
    $("#add-box").click(function() {
        if (chatBoxCount < 4) {
            chatBoxCount++;
            const newBox = createChatBox(chatBoxCount);
            $("#chat-boxes").append(newBox);
            adjustChatBoxLayout();
        }
    });

    // Event listener for removing a chat box
    $("#remove-box").click(function() {
        if (chatBoxCount > 1) {
            $("#chat-boxes .chat-box").last().remove();
            chatBoxCount--;
            adjustChatBoxLayout();
        }
    });

    // Event listener for refreshing chat boxes
    $("#refresh-box").click(function() {
        $(".output").text("Output will be shown here...");
        $(".chat-box").each(function(index) {
            $(this).replaceWith(createChatBox(index + 1));
        });
        adjustChatBoxLayout();
    });

    // Event listener for stopping response generation
    $("#stop-generation").click(function() {
        console.log("Stop generating response");
    });

    // Event listener for toggling overview button
    $("#overview").change(function() {
        if ($(this).is(":checked")) {
            $("#overview-output-cell").show();
            $("#overview-output-cell").html('<p>Overview:</p>');
        } else {
            $("#overview-output-cell").hide();
            $("#overview-output-cell").empty();
        }
    });
    

    // Event listener for radio buttons
    $(document).on('change', '.radio-label input[type="radio"]', function() {
        const model = $(this).val();
        const parentId = $(this).closest('.chat-box').attr('id');
        const select = $(this).closest('.input-group').find('.model-select select');
        select.prop('disabled', false);
        select.empty();
        select.append('<option value="">Select a model</option>');
        switch (model) {
            case 'gemini':
                select.append('<option value="gemini-1.0-pro">Gemini 1.0 Pro</option>');
                select.append('<option value="gemini-1.5-flash" selected>Gemini 1.5 Flash</option>');
                select.append('<option value="gemini-1.5-pro">Gemini 1.5 Pro</option>');
                break;
            case 'gpt':
                select.append('<option value="gpt-3.5-turbo" selected>GPT-3.5 Turbo</option>');
                break;
            case 'groq':
                select.append('<option value="llama3-8b-8192" selected>Llama 3 8B-8192</option>');
                select.append('<option value="llama3-70b-8192">Llama 3 70B-8192</option>');
                break;
        }
    });


    // Event listener for adding audience and role input bars
    $(document).on('click', '.add-input', function() {
        const type = $(this).data('type');
        const parentId = $(this).closest('.chat-box').attr('id');
        const inputField = `<input type="text" class="input-bar" id="${type}-${parentId}" placeholder="${type.charAt(0).toUpperCase() + type.slice(1)}" name="${type}-${parentId}">`;
        $(this).replaceWith(inputField);
        $(`#${type}-${parentId}`).fadeIn();
    });

    // Function to adjust the layout of chat boxes
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
