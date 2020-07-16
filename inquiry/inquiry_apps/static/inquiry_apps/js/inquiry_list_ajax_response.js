'use strict';


$(function () {
    $('#id_div_ajax_response').text('kitaaa');
    $.ajax({
        url: '/inquiry/list/ajax/response/',
        type: 'GET',
        data: params,
        dataType: 'html',
    })
    .done(function (data) {
        $('#id_div_ajax_response').html(data);
    });






});