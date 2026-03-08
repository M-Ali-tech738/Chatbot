css="""<style>
:root {
    --user-bg-color: #e4f1f5; /* Default user background color */
    --bot-bg-color: #f2f0f5; /* Default bot background color */
}

@media (prefers-color-scheme: dark) {
    :root {
        --user-bg-color: #2b313e; /* Dark mode user background color */
        --bot-bg-color:#475063; /* Dark mode bot background color */
    }
}

.chat_message {
    padding: 1.5em;
    border-radius: 0.5em;
    margin-bottom: 1em;
    display: flex;
}

.chat-message.user {
    background-color: var(--user-bg-color);
}

.chat-message.bot {
    background-color: var(--bot-bg-color);
}

.chat-message.avatar {
    width: 15%;
}
</style>
"""
bot_template = '''
<div class="chat-message bot">
    <div class="avatar"> 
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar"> 
    <div class="message">{{MSG}}</div>
</div>
'''