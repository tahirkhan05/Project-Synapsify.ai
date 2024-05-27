$(document).ready(function() {
  let boxCount = 1;
  let isGenerating = false;

  $('#add-box').click(function() {
      if (boxCount < 4) {
          boxCount++;
          $('#chat-boxes').append(
              `<div class="chat-box">
                  <div class="input-group">
                      <input type="text" id="audience-${boxCount}" placeholder="General Public ${boxCount}" name="audience-${boxCount}"><br><br>
                      <div class="radio-group">
                          <label class="radio-label">
                              <input type="radio" id="gemini-${boxCount}" name="model-${boxCount}" value="gemini">
                              <div class="radio-inner"></div>
                              <span>Gemini</span>
                          </label>
                          <label class="radio-label">
                              <input type="radio" id="gpt-${boxCount}" name="model-${boxCount}" value="gpt">
                              <div class="radio-inner"></div>
                              <span>GPT</span>
                          </label>
                          <label class="radio-label">
                              <input type="radio" id="groq-${boxCount}" name="model-${boxCount}" value="groq">
                              <div class="radio-inner"></div>
                              <span>Groq</span>
                          </label>
                      </div>
                  </div>
                  <div class="output-cell">
                      <h2>Output:</h2>
                      <p class="output"></p>
                  </div>
              </div>`
          );
      }
  });

  $('#remove-box').click(function() {
      if (boxCount > 1) {
          $('#chat-boxes .chat-box:last').remove();
          boxCount--;
      }
  });

  $('#refresh-box').click(function() {
      $('#chat-boxes').html(
          `<div class="chat-box">
              <div class="input-group">
                  <input type="text" id="audience-1" placeholder="General Public" name="audience-1"><br><br>
                  <div class="radio-group">
                      <label class="radio-label">
                          <input type="radio" id="gemini-1" name="model-1" value="gemini" checked="true">
                          <div class="radio-inner"></div>
                          <span>Gemini-1</span>
                      </label>
                      <label class="radio-label">
                          <input type="radio" id="Gpt-1" name="model-1" value="Gpt-1">
                          <div class="radio-inner"></div>
                          <span>GPT</span>
                      </label>
                      <label class="radio-label">
                          <input type="radio" id="Groq-1" name="model-1" value="Groq">
                          <div class="radio-inner"></div>
                          <span>Groq</span>
                      </label>
                  </div>
              </div>
              <div class="output-cell">
                  <h2>Output:</h2>
                  <p class="output"></p>
              </div>
          </div>`
      );
      boxCount = 1;
  });

  $('#chatbot-form').on('submit', function(event) {
      event.preventDefault();
      if (isGenerating) return;

      isGenerating = true;
      $.ajax({
          url: $(this).attr('action'),
          type: $(this).attr('method'),
          data: $(this).serialize(),
          success: function(response) {
              $('.output').each(function(index) {
                  const text = response['response' + (index + 1)];
                  let i = 0;
                  $(this).text('');
                  function typeWriter() {
                      if (!isGenerating) return;
                      if (i < text.length) {
                          $(this).append(text.charAt(i));
                          i++;
                          setTimeout(typeWriter.bind(this), 10);
                      }
                  }
                  typeWriter.call(this);
              });
          },
          complete: function() {
              isGenerating = false;
          }
      });
  });

  $('#stop-generation').click(function() {
      isGenerating = false;
  });
});
