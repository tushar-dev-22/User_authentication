"use strict";

var KTSigninGeneral = function() {
    var e, t, i;
    return {
        init: function() {
            e = $('#kt_sign_in_form'), t = $('#kt_sign_in_submit'), 
            i = FormValidation.formValidation(e[0], {
                fields: {
                    username: {
                        validators: {
                            notEmpty: {
                                message: "This field is required"
                            }
                        }
                    },
                    password: {
                        validators: {
                            notEmpty: {
                                message: "The password is required"
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: ".fv-row",
                        eleInvalidClass: "",
                        eleValidClass: ""
                    })
                }
            }), t.on("click", function(n) {
                n.preventDefault(), i.validate().then(function(i) {
                    if (i == 'Valid') {
                        toastr.info('Submitting the login form...');

                        $.ajax({
                            type: "POST",
                            url: e.attr('action'),
                            data: e.serialize(),
                            headers: {
                                "X-CSRFToken": getCookie("csrftoken")
                            },
                            success: function(response) {

                                if(response.status == 200){
                                    toastr.success('Login successful!');
                                    // redirect to another page
                                    window.location.href = response.data.redirect;

                                }else if(response.status==401){

                                    toastr.error(response.message);

                                }else if(response.status == 400){

                                    $('#email-error').text(response.message);
                                    $('#email-error').show();
                                    
                                }
                               
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                toastr.error('Login failed!');
                                // do something after failed login
                            }
                        });
                    } else {
                        toastr.error('All required fields!');
                    }
                });
            });
        }
    };
}();

KTUtil.onDOMContentLoaded(function() {
    KTSigninGeneral.init();
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}