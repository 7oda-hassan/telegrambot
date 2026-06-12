# Feature Compatibility Matrix

The following table demonstrates all Rich Markdown features supported by the native Telegram ecosystem, and their implementation status within this bot.

| Feature | Status | Notes |
|---------|--------|-------|
| **Headings (H1 - H6)** | Supported | Renders natively via `#` tokens. |
| **Checklists** | Supported | Renders as interactive `TaskNode` elements. |
| **Block Quotes** | Supported | Handled natively by Telegram payloads. |
| **Code Blocks (Pre)** | Supported | Preserves multiline spacing and language tags. |
| **Inline Code** | Supported | Handled natively via `code` entities. |
| **Bold** | Supported | Handled natively via `bold` entities. |
| **Italic** | Supported | Handled natively via `italic` entities. |
| **Strikethrough** | Supported | Handled natively via `strikethrough` entities. |
| **Spoiler** | Supported | Handled natively via `spoiler` entities. |
| **Underline** | Supported | Handled natively via `underline` entities. |
| **Standard Links** | Supported | Handled natively via `url` entities. |
| **Inline Text Links** | Supported | Handled natively via `text_link` entities. |
| **Email Links** | Supported | Handled natively via `email` entities. |
| **Phone Links** | Supported | Handled natively via `phone_number` entities. |
| **Custom Emoji** | Supported | Preserves premium Telegram emoji IDs. |
| **User Mentions** | Supported | Handled natively by Telegram payloads. |
| **Time Entities** | Supported | Handled natively by Telegram payloads. |
| **Math Blocks** | Supported | Processed natively if correctly formed by client. |
| **Tables** | Supported | Processed natively if correctly formed by client. |
| **Footnotes** | Supported | Processed natively if correctly formed by client. |

> [!NOTE]
> If a payload contains an invalid media URL preventing rich message compilation, the bot features a built-in safety fallback that strips the invalid embedded images and re-renders the text payload, guaranteeing 100% message delivery reliability.
