'use strict';


$(function () {


    function update_table(input_id='', input_email='', input_page='', input_word='', use_history='false'){
        var params = {
            id: input_id,
            email: input_email,
            page: input_page,
            word: input_word,
        }
        var query_string='';
        if (params.id || params.email || params.page || params.word) {
            var query_string = '?' + jQuery.param(params);
        };
        var url = '/inquiry/list/ajax/' + query_string;
        
        $.ajax({
            url: '/inquiry/list/ajax/response/',
            type: 'GET',
            data: params,
            dataType: 'html',
        })
        .done(function (data) {


            if (use_history == true) {
                history.pushState(null, null, url);
            };
            $('#id_div_ajax_response').html(data);
        })
        .fail(function() {
            alert('Ajax failed')
        });
    };



    function update_table_by_url() {
        var split_location_search = location.search.substring(1).split('&');
        var args_items = {};
        for (var i=0; split_location_search[i]; i++) {
            var split_items = split_location_search[i].split('=')
            args_items[(decodeURIComponent(split_items[0]))] = (decodeURIComponent(split_items[1]));
        };
        $('#id_id').val(args_items['id']);
        $('#id_email').val(args_items['email']);
        $('#id_page').val(args_items['page']);
        $('#id_word').val(args_items['wprd']);
        return args_items;
    };
    

    var args_items = update_table_by_url();
    update_table(args_items['id'], args_items['email'], args_items['page'], args_items['word']);

    // browser => get from URL
    $(window).on('popstate', function() {
        var args_items = update_table_by_url();
        update_table(args_items['id'], args_items['email'], args_items['page'], args_items['word']);
    });

    // when search 
    $('#inquiry_list_button').on('click', function(event) {
        event.preventDefault();
        var input_id = $('#id_id').val();
        var input_email = $('#id_email').val();
        var input_page = $('#id_page').val();
        var input_word = $('#id_word').val();      
        update_table(input_id, input_email, input_page, input_word, true);
    
    });

    // ajax paging
    $('#id_div_ajax_response').on('click', '#pager a', function(event) {
        event.preventDefault();
        var args_items = update_table_by_url();
        var page_num = $(this).text();
        $('#id_page').val(page_num);
        update_table(args_items['id'], args_items['email'], page_num, args_items['word'], true);
    });
});


