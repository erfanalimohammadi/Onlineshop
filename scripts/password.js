document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.querySelector('input[type="password"]');
    
    passwordInput.addEventListener("input", function() {
      const password = this.value;
  
      // Check if password length is greater than 6 characters
      const isLengthValid = password.length > 6;
  
      // Check if password contains at least one uppercase letter
      const hasUppercase = /[A-Z]/.test(password);
  
      // Check if password contains at least one lowercase letter
      const hasLowercase = /[a-z]/.test(password);
  
      // Check if password contains at least one digit
      const hasNumber = /\d/.test(password);
  
      // Combine all validation conditions
      const isValidPassword = isLengthValid && hasUppercase && hasLowercase && hasNumber;
  
      // Show error message if password is not valid
      if (!isValidPassword) {
        this.setCustomValidity("Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one number.");
      } else {
        this.setCustomValidity("");
      }
    });
  });