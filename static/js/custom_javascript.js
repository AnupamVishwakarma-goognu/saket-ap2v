/*$('#refer_and_earn_from').on('submit',function(){
	var refer_and_earn_data = $(this).serialize();
	console.log(refer_and_earn_data);
	var refer_and_earn_url = $(this).attr('action');
	$.ajax({
		url: refer_and_earn_url,
		type: 'POST',
		data: refer_and_earn_data,
		success: function(response){
			var web_protocol_w_slash = window.location.protocol + "//" + window.location.host + "/thankyou/"
			if(response.result == true){
				window.location.href = web_protocol_w_slash
			console.log(response);
			}
		}
	});
});
*/

$('#enquiryform').on('submit',function(e) {
	$('#cover-spin').show(0)
        e.preventDefault();
        var enquiry_post_data = $(this).serialize();
        var enquiry_post_url = $(this).attr('action');
        $.ajax({
                url: enquiry_post_url,
                type: 'POST',
                data: enquiry_post_data,
                success: function(response){
			$('#cover-spin').hide(0)
			var web_protocol_w_slash = window.location.protocol + "//" + window.location.host + "/thankyou/"
                        $('#rac').modal('hide');
                        window.location.href = web_protocol_w_slash
                },
                error: function(response){
                        alert("Error to send enquiry data" + response)
                        //window.location.href = window.location.href
                }
        });
});


$('#contact_popup_form').on('submit',function(e){
	$('#cover-spin').show(0)
        e.preventDefault();
        var contact_pop_data = $(this).serialize();
        var contact_pop_url = $(this).attr('action');
        $.ajax({
                url: contact_pop_url,
                type: 'POST',
                data: contact_pop_data,
                success: function(response){
			$('#cover-spin').hide(0)
			var web_protocol_w_slash = window.location.protocol + "//" + window.location.host + "/thankyou/"
			$('#rac').modal('hide');
			window.location.href = web_protocol_w_slash
                },
                error: function(response){
                        alert("Error to send enquiry data.")
                }
        });
});

setTimeout(removeKeyFromStorage,30000);
function removeKeyFromStorage(){
	sessionStorage.removeItem('rac_modal');
	if (pop_value != 'True'){
		$('#rac').modal('show');
	}
}

$('#rac').on('hidden.bs.modal', function (e) {
	sessionStorage.setItem('rac_modal', true);
	$.ajax({
		url: '/popup_session',
		type: 'GET',
		success: function(r){
			console.log(r.result);
		}
	});
});

if (sessionStorage.getItem('rac_modal') != "true"){
	setTimeout(popup,3000);
	function popup(){
		if (pop_value != 'True'){
			$('#rac').modal('show');
		}
	}
}
//setTimeout(popup,8000);
//function popup(){
//        $('#rac').modal('show');
//}
