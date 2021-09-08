var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var form = document.getElementById('payment-form');
var style = {
    base: {
        color: '#000'
    }, 
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style:style});
card.mount('#card-element');

card.addEventListener('change', function(event){
    var errorDiv = document.getElementById('card-errors');
    if(event.error){
        var html = `<span class="material-icons-outlined" style='color: #dc3545'>
                        close
                    </span>
                    <span style='color: #dc3545'>${event.error.message}</span>`;
        $(errorDiv).html(html);
    }else{
        errorDiv.textContent = '';
    }
});

form.addEventListener('submit', function(event) {
    event.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card
        }
    }).then(function(result){
        if(result.error){
            var errorDiv = document.getElementById('card-errors');
            var html = `<span class="material-icons-outlined" style='color: #dc3545'>close</span>
                        <span style='color: #dc3545'>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        }else{
            if(result.paymentIntent.status === 'succeeded'){
                form.submit();
            }
        }
    });

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
