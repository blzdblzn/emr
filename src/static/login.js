document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.querySelector('form');
  
  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Show loading indicator
    const submitButton = document.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    submitButton.textContent = 'Logging in...';
    submitButton.disabled = true;
    
    fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: username,
    password: password
  })
})
.then(response => {
  console.log('Response status:', response.status);
  return response.json();
})
.then(data => {
  console.log('Response data:', data);
      // Reset button
      submitButton.textContent = originalButtonText;
      submitButton.disabled = false;
      
      if (data.message === 'Login successful') {
        alert('Login successful!');
        // Store user info or token
        localStorage.setItem('user', JSON.stringify(data.user));
        // For now, just show success message
        // In a full implementation, you would redirect to a dashboard
        console.log('Logged in user:', data.user);
      } else {
        alert('Login failed: ' + (data.error || 'Invalid credentials'));
      }
    })
    .catch(error => {
      // Reset button
      submitButton.textContent = originalButtonText;
      submitButton.disabled = false;
      
      console.error('Error:', error);
      alert('Login failed. Please try again.');
    });
  });
});
