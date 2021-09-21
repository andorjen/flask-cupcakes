"use strict"

const $cupcakeSection = $('#cupcake-section');
const $container = $('#container');
const $cupcakeForm = $('#cupcake-form');

/** function to query the API and return a list of cupcake objects*/
async function getCupcakes() {
    const resp = await axios.get("/api/cupcakes");
    const cupcakes = resp.data.cupcakes;

    return cupcakes;
}

/** get all cupcakes and display on home page*/
async function getAndDisplayCupcakes() {
    const cupcakes = await getCupcakes();
    displayCupcakes(cupcakes);

}

/** function that takes a list of cupcake object and displays cupcakes on homepage */
function displayCupcakes(cupcakes) {

    for (let cupcake of cupcakes) {
        const $eachCupcake = $('<div>');
        $eachCupcake.addClass("col-3");
        $eachCupcake.html(`
            <img src='${cupcake.image}' class='img-thumbnail'></img>
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Rating: ${cupcake.rating}</p>`);
        $cupcakeSection.append($eachCupcake);
    }
}

/** take data from cupcake form, make API request and update DOM, then reset form */
async function handleCupcakeForm(evt) {  //move axios call into it's own function
    evt.preventDefault();

    const cupcakeInput = {
        flavor: $("#cupcake-flavor").val(),
        size: $("#cupcake-size").val(),
        rating: $("#cupcake-rating").val(),
        image: $("#cupcake-image").val()
    };

    const cupcake = await postCupcakeData(cupcakeInput);
    updateCupcakeSection(cupcake);

    $cupcakeForm.trigger("reset");
}

/** take object of cupcake info and write into database, return cupcake instance data */
async function postCupcakeData(cupcakeInput) {
    const cupcake = await axios({
        url: "/api/cupcakes",
        method: "post",
        data: cupcakeInput,
    });
    return cupcake.data.cupcake;
}

/** take input of cupcake object, update page listing with the cupcake */
function updateCupcakeSection(cupcake) {
    let $eachCupcake = $('<div>');

    $eachCupcake.addClass("col-3");
    $eachCupcake.html(`
            <img src='${cupcake.image}' class='img-thumbnail'></img>
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Rating: ${cupcake.rating}</p>`)
    $cupcakeSection.append($eachCupcake);
}


// add event listener to body, show all cupcakes on load
$(window).on('load', getAndDisplayCupcakes)  // breakup function

//add event listener to form submission, update page with added cupcake
$cupcakeForm.on("submit", handleCupcakeForm)