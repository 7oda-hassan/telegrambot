# Production Features

The Telegram Rich Markdown Bot is equipped with a clean, stable set of production features designed to provide rich content formatting and channel publishing capabilities.

## 1. Rich Markdown Engine
The core feature of the bot is converting standard text and markdown elements into native Telegram Rich Formatting.
- **Bold**: `**text**`
- **Italic**: `*text*`
- **Strikethrough**: `~~text~~`
- **Spoiler**: `||text||`
- **Underline**: `__text__`
- **Inline Code**: `` `text` ``
- **Code Blocks**: ```language\n code \n```
- **Links**: `[Text](URL)`
- **Custom Emojis**: standard Telegram native parsing.
- **Headings**: `# Heading 1`, `## Heading 2`
- **Checklists**: `* [ ] Task` or `* [x] Completed Task`

## 2. Session Isolation (Markdown Mode)
To ensure the bot does not accidentally trigger on standard conversational messages, parsing is locked behind a session switch.
- Users must explicitly trigger `/markdown` (or click `Start Markdown Session` on the menu) to enter Markdown Mode.
- Once a single markdown document is successfully parsed and a preview is generated, the bot safely drops the user back into normal conversational mode.
- Users can manually abort a session anytime using `/cancel`.

## 3. Role-Based Dynamic UI
Upon starting the bot (`/start`), the bot analyzes the user's ID against the database to grant roles. The UI dynamically changes depending on the user.

### Owner (Super Admin)
Configured strictly via the `OWNER_ID` environment variable.
- Access to all Markdown features.
- Can publish content.
- Can Add / Remove other Admins.
- Can Add / Remove Linked Channels.
- Can List Admins and Channels.

### Admin
Added by the Owner.
- Access to all Markdown features.
- Can publish content to any linked channel.
- Can view the list of channels.
- *Cannot modify roles or channels.*

### General User
Anyone else interacting with the bot.
- Can ONLY use `/markdown` to format their own text.
- *Cannot see publishing or management buttons.*

## 4. Channel Publishing System
For Owners and Admins, after a Markdown preview is successfully generated, an inline keyboard automatically appears offering to `Publish` or `Cancel`.
- Clicking `Publish` lists all linked channels.
- Selecting a channel instantly dispatches the formatted Rich Message to the channel.
- Drafts are cached temporarily during this flow and destroyed after publishing.
