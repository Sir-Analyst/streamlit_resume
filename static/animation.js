document.addEventListener('DOMContentLoaded', function() {
  // Step 1: Hide everything
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 1s ease 2.5s';
  
  const avatar = document.querySelector('.avatar-ring');
  
  // Step 2: Center avatar on screen
  avatar.style.position = 'fixed';
  avatar.style.top = '50%';
  avatar.style.left = '50%';
  avatar.style.transform = 'translate(-50%, -50%)';
  avatar.style.zIndex = '9999';
  avatar.style.width = '280px';
  avatar.style.height = '280px';
  avatar.style.opacity = '0';
  
  // Step 3: Animate avatar drop (after 500ms)
  setTimeout(() => {
    avatar.style.transition = 'all 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    avatar.style.transform = 'translate(-50%, -50%) scale(1)';
    avatar.style.opacity = '1';
  }, 500);
  
  // Step 4: Reveal page content (after 2.5s total)
  setTimeout(() => {
    document.body.style.opacity = '1';
  }, 2500);
  
  // Step 5: Return avatar home (after 3.5s total)
  setTimeout(() => {
    avatar.style.transition = 'all 0.8s ease';
    avatar.style.position = 'relative';
    avatar.style.top = 'auto';
    avatar.style.left = 'auto';
    avatar.style.transform = 'none';
    avatar.style.zIndex = 'auto';
    avatar.style.width = '';
    avatar.style.height = '';
  }, 3500);
});
