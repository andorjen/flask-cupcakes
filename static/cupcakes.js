const $cupcakeSection = $('#cupcake-section');
const $container = $('#container')

// function to query the API and get the cupcakes
async function get_cupcakes(){
    const resp = await axios.get("/api/cupcakes");
    console.log('repsonse',resp)
    let cupcakes = resp.data.cupcakes;

    return cupcakes
}

// get cupcakes and display on page

async function display_cupcakes(){
    let cupcakes = await get_cupcakes();
    console.log("this is cupcakes",cupcakes)

    for (let cupcake of cupcakes){
        let $eachCupcake = $('<div>');
        $eachCupcake.addClass("col-3")
        $eachCupcake.html(`
            <img src='${cupcake.image}' class='img-thumbnail'></img>
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Rating: ${cupcake.rating}</p>`)
        $cupcakeSection.append($eachCupcake)
    }
}

$(window).on('load',display_cupcakes)