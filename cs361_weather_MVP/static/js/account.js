// Send an alert when the user click submit button.

function onSubmitForm(e)
{   
    let r = confirm('The account info will be updated after confirmation.');
    if(!r){
        e.preventDefault();
    }
}

const account_form = document.getElementById('account_form');
account_form.addEventListener('submit', onSubmitForm);