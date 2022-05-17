// Send an alert when the user click register button.

function onSubmitForm(e)
{
    //e.preventDefault();
    let r = confirm('The user name cannot be changed once the account is created.');
    if(!r){
        e.preventDefault();
    }
    const form3Example1m = document.getElementById('form3Example1m');
    const form3Example1n = document.getElementById('form3Example1n');
    const city_input = document.getElementById('city_input');
    const zip_input = document.getElementById('zip_input');

    if(form3Example1m.checked){
        if(city_input.value == ''){
            alert('city is missing!!');
            e.preventDefault();
        }
        return true;
    }else if(form3Example1n.checked){
        if(zip_input.value == ''){
            alert('ZipCode is missing!!');
            e.preventDefault();
        }
        return true;
    }else{
        e.preventDefault();
    }
}

const register_form = document.getElementById('register_form');
register_form.addEventListener('submit', onSubmitForm);