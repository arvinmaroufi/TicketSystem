document.addEventListener('DOMContentLoaded', function() {
    const newTicketBtn = document.querySelector('.btn-primary');
    const ticketForm = document.querySelector('.ticket-form');
    const ticketTable = document.querySelector('.ticket-table');
    
    newTicketBtn.addEventListener('click', function(e) {
        if (e.target.textContent === 'تیکت جدید') {
            ticketForm.style.display = 'block';
            ticketTable.style.display = 'none';
        }
    });

    const viewButtons = document.querySelectorAll('.btn-primary:not(:first-child)');
    const ticketDetails = document.querySelector('.ticket-details');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            ticketDetails.style.display = 'block';
            ticketTable.style.display = 'none';
        });
    });
});
