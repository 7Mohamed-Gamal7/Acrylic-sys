document.addEventListener('DOMContentLoaded', function() {
  // Highlight active menu item
  const currentUrl = window.location.pathname;
  const menuLinks = document.querySelectorAll('.sidebar-menu a');
  
  menuLinks.forEach(link => {
    if (link.getAttribute('href') === currentUrl) {
      link.classList.add('active');
    }
    
    link.addEventListener('click', function() {
      menuLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // Responsive sidebar toggle for mobile
  const sidebarToggle = document.createElement('button');
  sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
  sidebarToggle.className = 'sidebar-toggle';
  sidebarToggle.style.display = 'none';
  
  document.querySelector('.main-content').prepend(sidebarToggle);
  
  sidebarToggle.addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('mobile-show');
  });

  // Handle responsive behavior
  function handleResponsive() {
    if (window.innerWidth <= 768) {
      sidebarToggle.style.display = 'block';
    } else {
      sidebarToggle.style.display = 'none';
      document.querySelector('.sidebar').classList.remove('mobile-show');
    }
  }

  window.addEventListener('resize', handleResponsive);
  handleResponsive();
});
