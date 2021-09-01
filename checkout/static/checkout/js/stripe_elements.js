/* Logic taken from Stripe documentation */

document.addEventListener('DOMContentLoaded', async () => {
    var stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
    var client_secret = $('#id_client_secret').text().slice(1, -1);
    var stripe = Stripe(stripe_public_key);
    var elements = stripe.elements();
    var form = document.getElementById('payment-form');
    var card = elements.create('card');
    card.mount('#card-element');
});

card.addEventListener('change', function(event){
    var errorDiv = document.getElementById('card-errors');
    if(event.error){
        var html = `<span class="material-icons-outlined">
                        close
                    </span>
                    <span>${event.error.message}</span>`;
        $(errorDiv).html(html);
    }else{
        errorDiv.textContent = '';
    }
});

form.addEventListener('submit', function(event) {
  event.preventDefault();
  card.update({ 'disabled': true});
  $('#submit-button').addEventListener('disabled', true);

  stripe.createToken(card).then(function(result) {
    if(result.error){
        var error_div = document.getElementById('card-errors');
        var html = `<span class="material-icons-outlined">
                        close
                    </span>
                    <span>${result.error.message}</span>`;
        $(errorDiv).html(html);
        card.update({
            disabled: false
        });
        $('#submit-button').addEventListener('disabled', false);
    }else{
        if(result.paymentIntent.status === 'succeeded'){
            form.submit();
        }
    }
  });
});

