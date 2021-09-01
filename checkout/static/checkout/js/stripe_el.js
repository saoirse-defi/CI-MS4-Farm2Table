console.log("Test Saoirse");

    var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
    var client_secret = $('#id_client_secret').text().slice(1, -1);
    var stripe = Stripe(stripe_public_key);
    var elements = stripe.elements();
    var form = document.getElementById('payment-form');
    var card = elements.create('card');
    card.mount('#card-element');