document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Add event listener, prevent default form submission, and call send_email
  document.querySelector('#compose-form').addEventListener('submit', function (event) {
    event.preventDefault();
    send_email();
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  // prevent page to be refreshed via form submission
  console.log('send_email function starts now');
  // Get email data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  console.log(recipients);
  console.log(subject);
  console.log(body);

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
      .then(response => {
        // return both status code, and parsed json
        return response.json().then(data => {
          return {
            status: response.status,
            data: data
          };
        });
      })
      .then(result => {
        console.log(result.data);
        if (result.status === 201) {
          load_mailbox('sent');
        } else {
          alert(result.data.error || "Something went wrong!")
        }
      })
      .catch(error => {
        alert(error.error || "Something went wrong...")
      });

}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Create a div for all the emails, that later we can reset
  let emailListDiv = document.createElement('div');
  emailListDiv.id = 'email-list';
  document.querySelector('#emails-view').appendChild(emailListDiv);



  fetch(`/emails/${mailbox}`)
      .then(response => {
        // if response is not ok, status outside 200-299
        if (!response.ok) {
          return response.text().then(text => {
            throw new Error(text);
          });
        }
        // If response is ok, return parsed json response
        return response.json();
      })
      .then(emails => {
        render_emails(emails);
        console.log(emails);
      })
      .catch( error => {
        console.error("There was an error fetching emails:", error.message);
        alert("Error fetching emails:" + error.message);
      });
}

function render_emails(emails) {
  const emailList = document.querySelector('#email-list');

  // Clear any emails from before
  emailList.innerHTML = '';

  emails.forEach(function (email) {
          console.log(email);

          // Create a div for each email
          const emailElement = document.createElement('div');
          emailElement.className = 'email-item';

          // create top row
          const topRow = document.createElement('div');
          topRow.className = 'email-top-row';

          const senderElement = document.createElement('p');
          senderElement.className = 'email-sender';
          senderElement.innerText = `from: ${email.sender}`;
          topRow.appendChild(senderElement);

          const recipientsElement = document.createElement('p');
          recipientsElement.className = 'email-recipients';
          recipientsElement.innerText = `to: ${email.recipients.join(', ')}`;
          topRow.appendChild(recipientsElement);

          emailElement.appendChild(topRow);

          // create bottom row
          const bottomRow = document.createElement('div');
          bottomRow.className = 'email-bottom-row';

          const subjectElement = document.createElement('p');
          subjectElement.className = 'email-subject';
          subjectElement.innerText = `subject: ${email.subject}`;
          bottomRow.appendChild(subjectElement);

          const timestampElement = document.createElement('p');
          timestampElement.className = 'email-timestamp';
          timestampElement.innerText = email.timestamp;
          bottomRow.appendChild(timestampElement);

          emailElement.appendChild(bottomRow);

          // set appropriate background color
          if (email.read) {
              emailElement.style.backgroundColor = 'white';
          } else {
              emailElement.style.backgroundColor = 'lightgrey';
          }

          // Append email to email list
          emailList.appendChild(emailElement);


        });
}
