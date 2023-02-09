document.addEventListener("DOMContentLoaded", () => {

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Define the 'request' function to handle interactions with the server
  function server_request(url, data={}, verb, callback) {
    return fetch(url, {
      credentials: 'same-origin',
      method: verb,
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(function(response) {
      if(callback)
        callback(response);
    })
    .catch(error => console.error('Error:', error));
  }

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Handle POST Requests
  let form = document.querySelector('form');
  let table = document.querySelector('.table');
  let template = document.querySelector('#new_row');

  form.addEventListener('submit', (event) => {
    // Stop the default form behavior
    event.preventDefault();

    // Grab the needed form fields
    const action = form.getAttribute('action');
    const method = form.getAttribute('method');
    const data = Object.fromEntries(new FormData(form).entries());

    // Submit the POST request
    server_request(action, data, method, function(response) {
      // Add the template row content to the table
      table.insertAdjacentHTML('beforeend', template.innerHTML);

      // Update the content of the newly added row
      let row = table.lastElementChild;
      let columns = row.querySelectorAll('span');
      columns[0].innerText = response['id'];
      columns[1].innerText = response['first_name'];
      columns[2].innerText = response['last_name'];
      columns[3].querySelector('a').href = '/user/' + response['id'];
      columns[4].querySelector('a').href = '/user/' + response['id'];
    });
  });

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Handle PUT and DELETE Requests
  table.addEventListener('click', (event) => {
    if(event.target.tagName == 'A') {
      event.preventDefault();

      // Submit the request
      action = event.target.dataset.action;
      if(action == 'update') {
        alert("Not implemented yet!");

        // TODO: The UI needs to be implemented to display an edit form first...

        // data = {'first_name': 'Tom', 'last_name': 'Jones'};
        // server_request(event.target.href, data, 'PUT', function(response) {
        //   // If successful, delete the row
        //   if(response.success) {
        //     location.reload();
        //   }
        // });

      }
      else if (action == 'delete') {
        server_request(event.target.href, {}, 'DELETE', function(response) {
          // If successful, delete the row
          if(response.success) {
            event.target.closest('.row').remove();
          }
        });
      }
    }
  });
});