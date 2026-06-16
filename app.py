import os
import gradio as gr
from huggingface_hub import InferenceClient

def get_default_token():
    # 1. Try to read from environment variable
    token = os.environ.get("HF_TOKEN", "").strip()
    if token:
        return token
        
    # 2. Try to read from local files
    for filename in ["token.txt", ".env"]:
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("HF_TOKEN="):
                            return line.split("=", 1)[1].strip()
                        elif line.startswith("hf_"):
                            return line
        except Exception:
            pass
            
    return ""

# Custom CSS for modern glassmorphism design (More colorful layout)
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --primary-glow: #6366f1;
    --secondary-glow: #ec4899;
    --accent-color: #8b5cf6;
    --btn-gradient: linear-gradient(135deg, #4f46e5 0%, #db2777 50%, #8b5cf6 100%);
    --panel-glow: rgba(99, 102, 241, 0.15);
}

body {
    background: radial-gradient(circle at 5% 10%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 95% 90%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
                linear-gradient(135deg, #f8fafc 0%, #eff6ff 50%, #f5f3ff 100%) !important;
    font-family: 'Outfit', sans-serif !important;
    min-height: 100vh;
    margin: 0;
    color: #0f172a !important;
}

/* Glassmorphism Outer Container */
.gradio-container {
    max-width: 1200px !important;
    margin: 40px auto !important;
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    border: 1px solid rgba(255, 255, 255, 0.6) !important;
    border-radius: 24px !important;
    box-shadow: 0 25px 60px rgba(99, 102, 241, 0.1) !important;
    padding: 30px !important;
}

/* Header Styles */
.header-container {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.15);
}

.header-container h1 {
    font-size: 3rem;
    font-weight: 800;
    color: #4f46e5 !important;
    margin: 0 0 10px 0;
    text-align: center;
}

.header-container p {
    color: #475569;
    font-size: 1.15rem;
    font-weight: 400;
    margin: 0;
}

/* Panel Columns styling (Vibrant border glow on hover) */
#settings-column, #input-column, #output-column {
    background: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 18px !important;
    padding: 20px !important;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.05) !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
}

#settings-column:hover, #input-column:hover, #output-column:hover {
    border-color: var(--primary-glow) !important;
    box-shadow: 0 15px 35px var(--panel-glow) !important;
    transform: translateY(-2px);
}

.panel-title {
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(to right, #4f46e5, var(--secondary-glow));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    letter-spacing: -0.2px;
    border-bottom: 1px dashed rgba(99, 102, 241, 0.2);
    padding-bottom: 8px;
}

/* Textboxes, Inputs and Dropdowns */
.gradio-container textarea, .gradio-container input, .gradio-container select {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    padding: 12px !important;
    transition: all 0.3s ease !important;
}

.gradio-container textarea:focus, .gradio-container input:focus, .gradio-container select:focus {
    border-color: var(--secondary-glow) !important;
    box-shadow: 0 0 10px var(--panel-glow) !important;
    background: #ffffff !important;
}

/* Labels */
.gradio-container label span {
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 6px !important;
}

/* Custom Scrollbar */
textarea::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
textarea::-webkit-scrollbar-track {
    background: rgba(99, 102, 241, 0.05);
    border-radius: 10px;
}
textarea::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.2);
    border-radius: 10px;
}
textarea::-webkit-scrollbar-thumb:hover {
    background: var(--primary-glow);
}

/* Character counter row */
.input-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: -8px;
    margin-bottom: 12px;
    padding: 0 4px;
    font-size: 0.85rem;
}

#char-counter {
    color: #64748b;
    font-weight: 400;
}

#char-counter.limit-warning {
    color: #f59e0b;
}

#input-validation-msg {
    color: #ef4444;
    font-weight: 500;
}

/* Primary Generate Button (Vibrant colorful gradient) */
#generate-btn {
    background: var(--btn-gradient) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 14px 20px !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(219, 39, 119, 0.25) !important;
    width: 100% !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

#generate-btn:hover:not(.loading) {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(219, 39, 119, 0.4) !important;
    filter: brightness(1.1);
}

#generate-btn:active:not(.loading) {
    transform: translateY(0) scale(1) !important;
}

#generate-btn.loading {
    background: #94a3b8 !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
    pointer-events: none;
}

/* Copy and Clear Buttons */
#copy-btn {
    background: rgba(79, 70, 229, 0.08) !important;
    color: #4f46e5 !important;
    border: 1px solid rgba(79, 70, 229, 0.2) !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

#copy-btn:hover {
    background: var(--btn-gradient) !important;
    border-color: transparent !important;
    color: white !important;
    transform: translateY(-1px);
}

#clear-btn {
    background: rgba(239, 68, 68, 0.05) !important;
    color: #dc2626 !important;
    border: 1px solid rgba(239, 68, 68, 0.15) !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

#clear-btn:hover {
    background: #dc2626 !important;
    border-color: transparent !important;
    color: white !important;
    transform: translateY(-1px);
}

/* Radio buttons customization */
.gradio-container .gr-radio {
    display: flex;
    gap: 15px;
}

/* Toast Notifications Container */
#toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.toast {
    min-width: 280px;
    max-width: 380px;
    padding: 14px 20px;
    border-radius: 12px;
    background: #ffffff;
    border: 1px solid rgba(99, 102, 241, 0.15);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
    color: #0f172a;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 12px;
    transform: translateX(120%);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
    opacity: 0;
}

.toast.show {
    transform: translateX(0);
    opacity: 1;
}

.toast-success {
    border-left: 4px solid var(--primary-glow);
}

.toast-error {
    border-left: 4px solid #ef4444;
}

.toast-warning {
    border-left: 4px solid #f59e0b;
}

.toast-info {
    border-left: 4px solid var(--accent-color);
}

.toast-icon {
    font-size: 1.2rem;
}

/* Features and Requirements Info Card */
.features-card {
    background: linear-gradient(135deg, rgba(219, 39, 119, 0.05) 0%, rgba(79, 70, 229, 0.05) 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px;
    padding: 16px;
    margin-top: 20px;
}

.features-card h4 {
    margin: 0 0 10px 0;
    color: var(--secondary-glow);
    font-weight: 700;
    font-size: 0.98rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.features-card ul {
    margin: 0;
    padding-left: 15px;
    font-size: 0.85rem;
    color: #475569;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.features-card li {
    list-style-type: none;
    position: relative;
    padding-left: 10px;
}

.features-card li::before {
    content: "•";
    color: #4f46e5;
    font-weight: bold;
    position: absolute;
    left: -10px;
}
"""

# Header HTML
html_header = """
<div class="header-container">
    <h1>AI Email Reply Gen</h1>
    <p>Generate highly-customized, tone-perfect email replies in seconds using Llama-3.3</p>
</div>
"""

def generate_reply(email, tone, custom_points, length, language, signature):
    """
    Validates inputs and calls the Hugging Face InferenceClient 
    using the meta-llama/Llama-3.3-70B-Instruct model.
    Attempts multiple providers (hf-inference, together, sambanova, groq, deepinfra)
    to handle provider-specific limitations or rate limits.
    """
    if not email or not email.strip():
        return "Error: Received email is empty. Please enter an email in the middle panel."
        
    token = get_default_token()
    if not token:
        return (
            "Error: Hugging Face API key is missing.\n\n"
            "To generate replies, you must configure the environment variable HF_TOKEN "
            "in your Hugging Face Space settings or locally."
        )

    # Compile size constraints
    length_str = "short and concise" if length == "Short" else ("medium length" if length == "Medium" else "detailed and thorough")

    # Structure the prompt for the LLM based on user constraints
    prompt = f"""Write an email reply for the email below.

Email Details & Constraints:
- Tone: {tone}
- Target Length: {length_str}
- Reply Language: {language}
"""

    if custom_points and custom_points.strip():
        prompt += f"- Key Points/Details to Include:\n{custom_points.strip()}\n"
        
    if signature and signature.strip():
        prompt += f"- Sign off the email as: {signature.strip()}\n"
        
    prompt += f"""
Received Email to Reply to:
{email}

Make sure the reply:
1. Perfectly matches the requested tone ({tone}).
2. Addresses the email context and incorporates all the specified key points.
3. Includes a suitable greeting and custom signature (if provided).
4. Is written in {language}.
5. Is grammatically correct and formatted as a professional email.
6. Does not contain any conversational intro/outro or meta-commentary outside of the email itself.
"""

    # List of text-generation providers supporting meta-llama/Llama-3.3-70B-Instruct
    providers = ["hf-inference", "together", "sambanova", "groq", "deepinfra"]
    errors = []

    for provider in providers:
        try:
            client = InferenceClient(
                provider=provider,
                api_key=token
            )
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            reply = response.choices[0].message.content
            if reply and reply.strip():
                return reply.strip()
        except Exception as e:
            errors.append(f"{provider}: {str(e)}")
            continue

    # If all providers failed, output detailed logs
    error_details = "\n".join(errors)
    return (
        "API Error: Failed to generate reply using Llama-3.3-70B-Instruct.\n\n"
        "Attempted providers returned the following errors:\n"
        f"{error_details}\n\n"
        "Please check:\n"
        "1. Is your Hugging Face API token valid and active?\n"
        "2. Does your token have access to the Hugging Face Serverless API?\n"
        "3. Are you connected to the internet?"
    )

# Gradio Block layout definition
with gr.Blocks(title="AI Email Reply Gen") as demo:
    # Render custom HTML Header
    gr.HTML(html_header)
        
    with gr.Row(elem_id="main-container"):
        # Column 1: Customization Parameters (Using scale=1, which is integer)
        with gr.Column(elem_id="settings-column", scale=1):
            gr.HTML("<h3 class='panel-title'>🎨 Customization</h3>")
            tone = gr.Dropdown(
                choices=["Professional", "Friendly", "Formal", "Polite", "Customer Support", "Apology", "Thank You", "Technical", "Sales", "Urgent", "Informational"],
                value="Professional",
                label="Reply Tone",
                elem_id="tone-dropdown"
            )
            
            length = gr.Radio(
                choices=["Short", "Medium", "Long"],
                value="Medium",
                label="Reply Length",
                elem_id="length-radio"
            )
            
            language = gr.Dropdown(
                choices=["English", "Spanish", "French", "German", "Japanese", "Chinese", "Italian", "Portuguese", "Korean"],
                value="English",
                label="Reply Language",
                elem_id="language-dropdown"
            )
            
            signature = gr.Textbox(
                label="Email Signature",
                placeholder="e.g., John Doe, Customer Success Manager",
                elem_id="signature-input"
            )
            
        # Column 2: Inputs
        with gr.Column(elem_id="input-column", scale=1):
            gr.HTML("<h3 class='panel-title'>✉️ Received Email</h3>")
            email_input = gr.Textbox(
                lines=8,
                label="Email Body",
                placeholder="Paste the email you received here...",
                elem_id="email-input"
            )
            
            # Interactive Character Counter + Validation Label
            gr.HTML("""
            <div class="input-info-row">
                <span id="char-counter">0 characters</span>
                <span id="input-validation-msg"></span>
            </div>
            """)
            
            gr.HTML("<h3 class='panel-title' style='margin-top:10px;'>💡 Key Points to Include</h3>")
            custom_points = gr.Textbox(
                lines=4,
                label="Custom Instructions (Optional)",
                placeholder="e.g., Accept the meeting invite, but suggest Thursday at 2 PM instead of Wednesday...",
                elem_id="custom-points-input"
            )
            
            generate_btn = gr.Button("✨ Generate Reply", elem_id="generate-btn", variant="primary")
            
        # Column 3: Output & Features Description
        with gr.Column(elem_id="output-column", scale=1):
            gr.HTML("<h3 class='panel-title'>✨ Generated Reply</h3>")
            output = gr.Textbox(
                lines=10,
                label="Draft Reply",
                placeholder="AI-generated reply will appear here...",
                elem_id="output-reply"
            )
            
            with gr.Row():
                copy_btn = gr.Button("📋 Copy Reply", elem_id="copy-btn")
                clear_btn = gr.Button("🗑️ Clear All", elem_id="clear-btn")


    # Custom Javascript Setup on UI Load
    init_js = """
    () => {
        // 1. Inject Toast Container to DOM if not already present
        if (!document.getElementById('toast-container')) {
            const tc = document.createElement('div');
            tc.id = 'toast-container';
            document.body.appendChild(tc);
        }

        // 2. Define global helper for displaying notifications
        window.showToast = (message, type = 'success') => {
            const container = document.getElementById('toast-container');
            if (!container) return;

            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            
            let icon = '✨';
            if (type === 'success') icon = '✅';
            else if (type === 'error') icon = '❌';
            else if (type === 'warning') icon = '⚠️';
            else if (type === 'info') icon = 'ℹ️';

            toast.innerHTML = `
                <span class="toast-icon">${icon}</span>
                <div class="toast-content">${message}</div>
            `;

            container.appendChild(toast);
            
            // Trigger animation slide-in
            setTimeout(() => toast.classList.add('show'), 50);

            // Auto-dismiss toast after 3.5 seconds
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        };

        // 3. Poll to verify elements are injected and bind event listeners
        const checkElements = setInterval(() => {
            const emailTextarea = document.querySelector("#email-input textarea");
            const outputTextarea = document.querySelector("#output-reply textarea");
            const generateBtn = document.querySelector("#generate-btn");
            const copyBtn = document.querySelector("#copy-btn");
            const clearBtn = document.querySelector("#clear-btn");
            const counterDiv = document.getElementById("char-counter");
            const validationMsg = document.getElementById("input-validation-msg");

            if (emailTextarea && outputTextarea) {
                clearInterval(checkElements);

                // Function to update the character counter
                const updateCounter = () => {
                    const count = emailTextarea.value.length;
                    if (counterDiv) {
                        counterDiv.textContent = `${count} characters`;
                        if (count > 2000) {
                            counterDiv.classList.add('limit-warning');
                        } else {
                            counterDiv.classList.remove('limit-warning');
                        }
                    }

                    // Auto clear validation message if user types
                    if (count > 0 && validationMsg && validationMsg.textContent) {
                        validationMsg.textContent = "";
                    }
                };

                // Listen to keyboard/input events
                emailTextarea.addEventListener("input", updateCounter);
                
                // Secondary interval check to catch programmatic state updates
                setInterval(updateCounter, 150);

                // Bind custom client side Copy functionality
                if (copyBtn) {
                    copyBtn.onclick = (e) => {
                        e.preventDefault();
                        const reply = outputTextarea.value;
                        if (!reply || !reply.trim() || reply.startsWith("AI-generated reply will appear")) {
                            window.showToast("Nothing to copy yet!", "warning");
                            return;
                        }

                        navigator.clipboard.writeText(reply).then(() => {
                            window.showToast("Reply copied to clipboard!", "success");
                        }).catch(err => {
                            window.showToast("Failed to copy. Please select and copy manually.", "error");
                        });
                    };
                }

                // Clear Button Trigger message
                if (clearBtn) {
                    clearBtn.addEventListener("click", () => {
                        window.showToast("Cleared inputs!", "info");
                    });
                }
            }
        }, 100);
    }
    """

    # Chain JS initialization to blocks load event
    demo.load(js=init_js)


    # Event binding for Generation
    generate_btn.click(
        fn=generate_reply,
        inputs=[email_input, tone, custom_points, length, language, signature],
        outputs=output,
        js="""
        (email, tone, custom_points, length, language, signature) => {
            if (!email || !email.trim()) {
                window.showToast("Please enter a received email first!", "error");
                const validationMsg = document.getElementById("input-validation-msg");
                if (validationMsg) {
                    validationMsg.textContent = "Email is required";
                }
                throw new Error("Validation failed: Email input is empty");
            }
            
            const btn = document.querySelector("#generate-btn");
            if (btn) {
                btn.classList.add("loading");
                btn.textContent = "⏳ Generating Reply...";
            }
            return [email, tone, custom_points, length, language, signature];
        }
        """
    ).then(
        fn=None,
        js="""
        () => {
            const btn = document.querySelector("#generate-btn");
            if (btn) {
                btn.classList.remove("loading");
                btn.textContent = "✨ Generate Reply";
            }
        }
        """
    )

    # Clear button action (returns empty string for inputs & outputs, leaves key, signature, etc.)
    clear_btn.click(
        fn=lambda: ("", "", ""),
        inputs=None,
        outputs=[email_input, custom_points, output]
    )
if __name__ == "__main__":
    while True:
        try:
            demo.launch(css=custom_css)
            break
        except KeyboardInterrupt:
            print("\n[Warning] Server was interrupted. Relaunching server...")
            continue
