var stripe = Stripe("pk_test_51H1bR1GdhDRJjjYjUmaTube1tBLb166TMmqY7xdfkmd2LJhGTDvxHI3OtdvnqfkQyJcLmSAwoYe1IC3qHO95g1mp00CRHgsKXV");

var checkoutButton = document.getElementById("checkout-button");

checkoutButton.addEventListener("click", function () {
  fetch("/create-checkout-session", {
    method: "POST",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
      return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function (result) {
      // If redirectToCheckout fails due to a browser or network
      // error, you should display the localized error message to your
      // customer using error.message.
      if (result.error) {
        alert(result.error.message);
      }
    })
    .catch(function (error) {
      console.error("Error:", error);
    });
});