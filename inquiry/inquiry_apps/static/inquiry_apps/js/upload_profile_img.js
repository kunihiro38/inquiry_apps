'use strict';

function sendFileToServer(formData, status){
    var uploadURL = '/inquiry/edit/profile/avator/';
    var jqXHR = $.ajax({
        // The following are the parameters to pass to $ .ajax
        xhr: function() {
            // XMLHttpRequest (XHR) => JavaScriptなどのウェブブラウザ搭載のスクリプト言語でサーバとのHTTP通信を行うための、組み込みオブジェクト（API）
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                // addEventListner
                xhrobj.upload.addEventListener('progress', function(event){
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total = event.total;
                }, false);
            }
            return xhrobj;
        },
        url: uploadURL,
        type: 'POST',
        contentType: false,
        processData: false,
        cache: false,
        data: formData,
        dataType: 'json',
    })
        .done(function (data) {
            if (data['success'] === true) {
                // alert('success!');
                $('.edit-profile-table tbody tr td img').remove();
                $('#ajax-response')
                    .html(
                        '<img src="/media/' +
                        data['profile_img_path'] +
                        '" class="avator" >'
                    );
            }else {
                // alert('false');
                $('#preview').remove();
            };
        })
        .fail(function() {
            alert('Ajax failed');
        });
}


// drag and drop event
$(document).ready(function() {
    var obj = $("#dragandrophandler");
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function(e) {
        $(this).css('border', '2px dotted #0B85A1');
        e.preventDefault();

        var files = e.originalEvent.dataTransfer.files;
        
        // Modal dialog
        popupImage(files, obj);
    });

    // Avoid opening in a browser if the file is dropped outside the div
    $(document).on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $(document).on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        obj.css('border', '2px dotted #0B85A1');
    });

    $(document).on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });    
})

// modal dialog
function popupImage(files, obj) {
    var popup = document.getElementById('js-popup');
    if (!popup) return;

    var fd = new FormData();
    var filetype = files[0].type;

    $('.errorlist').remove();

    // 1. File format
    if (!(filetype.match('^image\/(png|jpeg)$'))){
        $('#dragandrophandler').after('<ul class="errorlist"><li>File formats other than png or jpeg cannot be used.</li></ul>');
        return false;
    }

    // 2. File size
    var sizeKB = files[0].size / 1024;
    if (parseInt(sizeKB) > 1024) {
        var sizeMB = sizeKB / 1024;
        if (sizeMB > 20) {
            $('#dragandrophandler').after('<ul class="errorlist"><li>The image size is too large. Please put an image smaller than 20MB.</li></ul>');
            return false;
        };
    };

    fd.append('avator', files[0])

    // preview
    var fileReader = new FileReader();
    fileReader.onloadend = function () {
        $('#popup-preview').html('<img src="' + fileReader.result + '"/>');
        // resize class
        $('#popup-preview img').addClass('resize_prev_img', 'item');
    }
    fileReader.readAsDataURL(files[0]);

    // close
    var blackBg = document.getElementById('js-black-bg');
    var closeBtn = document.getElementById('js-close-btn');
    var showBtn = document.getElementById('js-show-popup');
    var popupBtnN = document.getElementById('popup-btn-n');

    popup.classList.add('is-show');

     // btn is yes or no
    $('#popup-btn-y').off('click');
    $('#popup-btn-y').on('click', function () {
         // $('ul.errorlist').remove();
         // send file to server
        sendFileToServer(fd, status);
        popup.classList.remove('is-show');
        $('#dragandrophandler+div.statusbar').remove();
    });

    // call function
    closePopUp(blackBg);
    closePopUp(closeBtn);
    closePopUp(showBtn);
    closePopUp(popupBtnN);
    // close
    function closePopUp(elem) {
        if (!elem) return;
        elem.addEventListener('click', function () {
            popup.classList.remove('is-show');
            $('#dragandrophandler+div.statusbar').remove();
        });
    };
};
