$(document).ready(function() {
    $('#update_piece_title_button_id').click(function() {
	var pieceTitle = $('#piece_title_input_id').val();
	if ( pieceTitle.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'changePieceTitle':pieceTitle}, function(data) {  
		$('#piece_title_input_id').val(data.changePieceTitle);
	    });
	}
    });

    $('#e_name_submit').click(function() {
	var eName = $('#update_e_name').val();
	if ( eName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'name':eName}, function(data) {  
		$('#update_e_name').val(data.name);
	    });
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
    $('.remove_char_event').live('click',function() {
	var eCharName = $(this).parent().find('.first_name').text();
	eCharName += $(this).parent().find('.middle_name').text();
	eCharName += $(this).parent().find('.last_name').text();
	var parentElement = $(this).parent();
	if ( eCharName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'charName':eCharName}, function(data) {  
		$(parentElement).remove();
		$(parentElement).find('.remove_char_event').text('Add to event')
		$(parentElement).find('.remove_char_event').attr('class','add_char_event');
		$(parentElement).attr('class','char_name_piece');
		$('#chars_not_in_event_ul').append(parentElement);
	    });
	}
    });
    $('.add_char_event').live('click',function() {
	var eCharName = $(this).parent().find('.first_name').text();
	eCharName += $(this).parent().find('.middle_name').text();
	eCharName += $(this).parent().find('.last_name').text();
	var parentElement = $(this).parent();
	if ( eCharName.length ) {
	    var loc = $('#path').text();
	    $.post(loc, {'addCharacter':eCharName}, function(data) {  
		$(parentElement).remove();
		$(parentElement).find('.add_char_event').text('Remove from event')
		$(parentElement).find('.add_char_event').attr('class','remove_char_event');
		$(parentElement).attr('class','char_name_event');
		$('#chars_in_event_ul').append(parentElement);
	    });
	}

    });
    $('.update_name').click(function() {
	var c_name_piece = $(this).parent().find('input').val();
	if ( c_name_piece.length )
	{
	    var parentElement = $(this).parent();
	    var loc = $('#path').text();
	    $.post(loc, {'changeCName':c_name_piece, 'name_type':$(parentElement).attr('id')}, function(data) {  
		$(parentElement).find('input').val(data.c_name_piece);
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
