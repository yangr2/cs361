function onSubmit(){
    const radio  = document.querySelector('input[name="localType"]:checked').value;
    const cityInput = document.getElementById('city');
    const zipInput = document.getElementById('zip');
    const state = document.getElementById('form3Example4cdg').value;
    const appID = 'bcf0902c0d1c489fd50af46d16a775e2';
    let city = '';
    let zip = '';
    if(radio == 'city'){
        city = cityInput.value.trim();
        getDataByCity(state,city,appID);
    }else{
        zip = zipInput.value.trim();
        getDataByZip(state,zip,appID);
    }

    


}

function getDataByCity(state,city,appID){
    const data = {city: city, state: state, appID: appID};
    fetch('geocoding', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const { main, name, sys, weather } = data;
        const list = document.querySelector(".ajax-section .cities");
        const icon = `https://s3-us-west-2.amazonaws.com/s.cdpn.io/162656/${
          weather[0]["icon"]
        }.svg`;
  
        const li = document.createElement("li");
        li.classList.add("city");
        const markup = `
          <h2 class="city-name" data-name="${name},${sys.country}">
            <span>${name}</span>
            <sup>${sys.country}</sup>
          </h2>
          <div class="city-temp">${Math.round(main.temp)}<sup>°C</sup></div>
          <figure>
            <img class="city-icon" src="${icon}" alt="${
          weather[0]["description"]
        }">
            <figcaption>${weather[0]["description"]}</figcaption>
          </figure>
        `;
        li.innerHTML = markup;
        list.innerHTML = '';
        list.appendChild(li);
      })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function getDataByZip(state,zip,appID){
    const data = {zip:zip, state: state, appID: appID};
    fetch('geocoding', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const { main, name, sys, weather, wind  } = data;
        const list = document.querySelector(".ajax-section .cities");
        const icon = `https://s3-us-west-2.amazonaws.com/s.cdpn.io/162656/${
          weather[0]["icon"]
        }.svg`;
  
        const li = document.createElement("li");
        li.classList.add("city");
        const markup = `
          <h2 class="city-name" data-name="${name},${sys.country}">
            <span>${name}</span>
            <sup>${sys.country}</sup>
          </h2>
          <div class="city-temp">${Math.round(main.temp)}<sup>°C</sup></div>
          <figure>
            <img class="city-icon" src="${icon}" alt="${
          weather[0]["description"]
        }">
            <figcaption>${weather[0]["description"]}</figcaption>
          </figure>
        `;
        li.innerHTML = markup;
        list.innerHTML = '';
        list.appendChild(li);
      })
    .catch((error) => {
        console.error('Error:', error);
    });
}

const submit = document.getElementById('search');
submit.addEventListener('click', onSubmit);

document.addEventListener("DOMContentLoaded", function(){
    // Handler when the DOM is fully loaded
    submit.click();
});