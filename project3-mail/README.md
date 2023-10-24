# Project Mail: An email application

- [App Demo on Youtube](https://youtu.be/6VQjBqlFcQU)
- [Project Instructions](https://cs50.harvard.edu/web/2020/projects/3/mail/)


A simple web-based email client with functionalities like composing emails, viewing inbox, sent, and archived emails.

## Features:

- **Compose Email**: Users can write and send emails.
- **Mailbox Views**: View `inbox`, `sent`, and `archive` emails.
- **Single Email View**: Allows users to view the entire email along with options to `Reply` and `Archive/Unarchive`.
- **Toggle Email Read Status**: Unread emails are differentiated by color for easy spotting.
- **Responsive UI**: Switches views seamlessly based on the user's interactions.
- **Error Handling**: Captures and displays errors effectively during API fetch operations.

## Usage:

1. **Navigation**
    - Click on `inbox`, `sent`, or `archived` to view respective emails.
    - Click on `compose` to draft a new email.
   
2. **Composing an Email**
    - Fill in the recipient's email, subject, and body.
    - Click the send button to dispatch the email.
   
3. **Viewing an Email**
    - Click on any email from the list to open and read its content.
    - If the email was sent by someone else and not the logged-in user, options to `Archive` or `Unarchive` are available.
    - Use the `Reply` button to respond to the email.
   
4. **Archiving an Email**
    - Click on the `Archive` or `Unarchive` button based on the email's current status.
