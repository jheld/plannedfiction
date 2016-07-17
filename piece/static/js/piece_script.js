$(document).ready(function() {
    $('#submit_piece_id').click(function() {  
	var newTitle = $(this).parent().find('#id_title').val();
	var parentElement = $(this).parent();
	if ( newTitle.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'newTitle':newTitle}, function(data) {  
		if ( data['piecePK'] && data['pieceTitle'])
		{
		    var newLI = document.createElement('li');
		    newLI.setAttribute('class','piece_li_class');
		    var newA = document.createElement('a');
		    newA.innerHTML = data['pieceTitle'];
		    newA.setAttribute('href','/pieces/'+data['piecePK']+'/');
		    newLI.appendChild(newA);
		    $('#pieces_ul_id').append(newLI);
		}
	    });
	}

	
    });
    // Test code for no update button needed in piece.html title update
    $('#piece_title_input_id').change(function() {
	var pieceTitle = $('#piece_title_input_id').val();
	if ( pieceTitle.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'changePieceTitle':pieceTitle}, function(data) {  
		$('#piece_title_input_id').val(data.changePieceTitle);
		if ( data['title_error'].toString().length > 0 )
		{
		    alert(data['title_error'].toString());
		}
	    });
	}
    });

    // try the contenteditable piece title, instead of "input" element
    $("#piece_title_p_id").change(function() {
	var pieceTitle = $("#piece_title_p_id").val();
	alert(pieceTitle);
    })
    // end piece title contenteditable

    $('#e_name_submit').click(function() {
	var eName = $('#update_e_name').val();
	if ( eName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'e_name':eName}, function(data) {  
		$('#update_e_name').val(data['e_name']);
	    });
	}
    });
    if ( !$('#chars_not_in_event_ul li').text().length )
    {
	$('#chars_not_in_event_ul').append('<li id="no_chars">No characters not included</li>');
    }
    
    $('body').on('change', '#chars_not_in_event_ul',function() {
	alert('hi');
	if ( !$('#chars_not_in_event_ul li').size() )
	{
	    $('#chars_not_in_event_ul').empty();
	}
	else
	{
	    $('#chars_not_in_event_ul').firstChild().remove();
	}
    });

    $('#e_description_submit').click(function() {
	var eDescription = $('#update_e_description').val();
	if ( eDescription.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'description':eDescription}, function(data) {  
		$('#update_e_description').val(data.description);
	    });
	}
    });
    $('#e_order_submit').click(function() {
	var e_order = $('#e_order').val();
	if ( e_order.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'e_order':e_order}, function(data) {  
		$('#e_order').val(data.e_order);
	    });
	}
    });
    $('body').on('click', '.remove_char_event',function() {
	var eCharName = $(this).parent().find('.name').text();
	var parentElement = $(this).parent();
	if ( eCharName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'charName':eCharName}, function(data) {  
		$(parentElement).remove();
		
		$('#chars_not_in_event_ul').find('#no_chars').remove();
		$(parentElement).find('.remove_char_event').text('Add to event')
		$(parentElement).find('.remove_char_event').attr('class','add_char_event');
		$(parentElement).attr('class','char_name');
		$('#chars_not_in_event_ul').append(parentElement);
	    });
	}
    });
    $('body').on('click', '.add_char_event',function() {
	var eCharName = $(this).parent().find('.name').text();
	var parentElement = $(this).parent();
	if ( eCharName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'addCharacter':eCharName}, function(data) {  
		$(parentElement).remove();
		if ( !$('#chars_not_in_event_ul li').size() )
		{
		    $('#chars_not_in_event_ul').append('<li id="no_chars">No characters not included</li>');
		}
		$(parentElement).find('.add_char_event').text('Remove from event')
		$(parentElement).find('.add_char_event').attr('class','remove_char_event');
		$(parentElement).attr('class','char_name_event');
		$('#chars_in_event_ul').append(parentElement);
	    });
	}

    });
    
    $('.update_name').click(function() {

	    var c_name = $(this).parent().find('#c_name_input').val();
	    if ( c_name.length )
	    {
	        var parentElement = $(this).parent();
	        var loc = $('#path').text();
	        $.post(loc, {'changeCName':c_name, 'name_type':$(parentElement).attr('id')}, function(data) {  
		        $(parentElement).find('#c_name_input').val(data.c_name);
	        });	    
	    }
    });
    $('.update_age').click(function() {
	var c_age = $(this).parent().find('input').val();
	if ( c_age.length )
	{
	    var parentElement = $(this).parent();
	    var loc = $('#path').text();
	    $.post(loc, {'changeCAge':c_age}, function(data) {  
		    $(parentElement).find('input').val(data['changeCAge']);
	    });	    
	}
    });
    $('.update_gender').click(function() {
	var c_gender = $(this).parent().find('input').val();
	if ( c_gender.length )
	{
	    var parentElement = $(this).parent();
	    var loc = $('#path').text();
	    $.post(loc, {'changeCGender':c_gender}, function(data) {  
		$(parentElement).find('input').val(data['changeCGender']);
	    });	    
	}
    });
    $('#character_search_submit').click(function() {
	var character_search_input = $(this).parent().find('#character_search_input').val();
    character_search_input = character_search_input.replace(/^\s+/,'');
    character_search_input = character_search_input.replace(/\s+$/,'');
    $(this).parent().find('#character_search_input').val(character_search_input);
	if ( character_search_input.length )
	{
	    var parentElement = $(this).parent();
	    var loc = $('#path').text();
	    $.get(loc, {'character_search_input':character_search_input}, function(data) {  
		$('#character_results_header').show('slow');
		$(document).find('#character_results_ul').empty();
		if ( data['characters_results'].length == 1 && data['characters_results'].toString().indexOf(',') == -1 )
		{
		    $(document).find('#character_results_ul').append('<li>'+data['characters_results'][0].toString()+'</li>');
		}
		else
		{
		    for ( var i = 0; i < data['characters_results'].length; i++  )
		    {
			var result_str = data['characters_results'][i];
			$(document).find('#character_results_ul').append('<li><a href=pieces/'+result_str[1]+'/characters/'+result_str[2]+'>'+result_str[0].toString()+'<ul><li><a href="pieces/'+result_str[1]+'/">'+result_str[3]+'</a></li></ul></li>');		    
		    }
		    
		}
	    });	    
	}
    });

});
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function allowDrop(ev) {    
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("Text",ev.target.id);
}

function drop(ev) {
    var data = ev.dataTransfer.getData("Text");
    ev.target.appendChild(document.getElementById(data));
    ev.preventDefault();
}
