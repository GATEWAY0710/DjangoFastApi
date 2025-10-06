const loadUsersBtn = document.getElementById('loadUsersBtn');
const usersTable = document.getElementById('usersTable');
const usersTableBody = usersTable.querySelector('tbody');
const loader = document.getElementById('loader');
const errorAlert = document.getElementById('errorAlert');

loadUsersBtn.addEventListener('click', async () => {
    // Reset UI
    usersTable.classList.add('d-none');
    errorAlert.classList.add('d-none');
    loader.style.display = 'block';

    try {
        // Fetch data from API
        var token = localStorage.getItem("access_token")
        const response = await fetch('http://127.0.0.1:8000/users', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.status === 401){
            console.error("Invalid token used");
            window.location.href = "login.html"
        }
        const data = await response.json();
        let users = data.users

        // Clear previous data
        usersTableBody.innerHTML = '';

        // Populate table rows
        users.forEach((user) => {
            const row = `
            <tr>
              <th scope="row">${user.id}</th>
              <td>${user.username}</td>
              <td>${user.email}</td>
            </tr>`;
            usersTableBody.insertAdjacentHTML('beforeend', row);
        });

        // Show table
        loader.style.display = 'none';
        usersTable.classList.remove('d-none');
    } catch (error) {
        console.error(error);
        loader.style.display = 'none';
        errorAlert.classList.remove('d-none');
    }
});