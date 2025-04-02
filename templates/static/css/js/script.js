document.addEventListener('DOMContentLoaded', () => {
    console.log('Aplicação carregada com Flask + Bootstrap!');
  
    // Validação do formulário de registro (se existir na página)
    const registerForm = document.getElementById('registerForm');
    if(registerForm) {
      registerForm.addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        if(password !== confirmPassword) {
          e.preventDefault();
          alert('As senhas não coincidem. Por favor, verifique.');
        }
      });
    }
  });
  