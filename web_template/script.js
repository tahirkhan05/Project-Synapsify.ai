// Get all nav links
const navLinks = document.querySelectorAll('.nav-link');

// Add event listener to each nav link
navLinks.forEach(link => {
    link.addEventListener('click', event => {
        // Prevent default link behavior
        event.preventDefault();

        // Get the href attribute of the link
        const href = link.getAttribute('href');

        // Scroll to the section with the corresponding id
        document.querySelector(href).scrollIntoView({
            behavior: 'mooth'
        });
    });
});