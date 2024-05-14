window.addEventListener('DOMContentLoaded', function() {
    const bottom = document.querySelector('#content').scrollHeight;
    const bottomElement = document.createElement('div');
    bottomElement.id = 'bottom';
    bottomElement.style.height = '1px';
    bottomElement.style.width = '1px';
    bottomElement.style.overflow = 'hidden';
    document.body.appendChild(bottomElement);
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('scroll')) {
      window.scrollTo({ top: bottom, behavior: 'smooth' });
    }
  });