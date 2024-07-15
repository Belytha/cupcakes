function createCupcakeHTML(cupcake) {
  /** Creates cupcake HTML */
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="cupcake-img" src="${cupcake.image}" alt="(no image provided)">
      </div>
    `;
  }

async function showAllCupcakes(){
  /**Gets cupcakes from api and shows all cupcakes on page */
    const response = await axios.get('/api/cupcakes');
    for (let cupcake of response.data.cupcakes){
      let newCupcake = $(createCupcakeHTML(cupcake));
      $('#cupcakes-list').append(newCupcake);
    }
}


$('form').on("submit", async function(evt){
  /**Handles form for submitting new cupcake */
  evt.preventDefault();

  let flavor = $('#flavor').val();
  let rating = $('#rating').val();
  let size = $('#size').val();
  let image = $('#image').val();

  const cupcakeResp = await axios.post('/api/cupcakes', {flavor, rating, size, image});

  let newCupcake = $(createCupcakeHTML(cupcakeResp.data.cupcake))
  $('#cupcakes-list').append(newCupcake);
  $('form').trigger('reset');
});

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`/api/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(showAllCupcakes());