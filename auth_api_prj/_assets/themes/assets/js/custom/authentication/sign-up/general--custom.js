"use strict";
var KTSignupGeneral = (function () {
    var e,
        t,
        a,
        r,
        s = function () {
            return 100 === r.getScore();
        };
    return {
        init: function () {
            (e = document.querySelector("#kt_sign_up_form")),
                (t = document.querySelector("#kt_sign_up_submit")),
                (r = KTPasswordMeter.getInstance(e.querySelector('[data-kt-password-meter="true"]'))),
                (a = FormValidation.formValidation(e, {
                    fields: {
                        "first-name": { validators: { notEmpty: { message: "First Name is required" } } },
                        "last-name": { validators: { notEmpty: { message: "Last Name is required" } } },
                        email: { validators: { regexp: { regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "The value is not a valid email address" }, notEmpty: { message: "Email address is required" } } },
                        password: {
                            validators: {
                                notEmpty: { message: "The password is required" },
                                callback: {
                                    message: "Please enter valid password",
                                    callback: function (e) {
                                        if (e.value.length > 0) return s();
                                    },
                                },
                            },
                        },
                        "confirm-password": {
                            validators: {
                                notEmpty: { message: "The password confirmation is required" },
                                identical: {
                                    compare: function () {
                                        return e.querySelector('[name="password"]').value;
                                    },
                                    message: "The password and its confirm are not the same",
                                },
                            },
                        },
                        phone_number: {
                            validators: {
                                regexp: { regexp: /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im},
                                notEmpty: { message: "The phone number is not valid" },
                            
                                    message: "Please enter valid phone number",
                            
                            },
                        },
                        toc: { validators: { notEmpty: { message: "You must accept the terms and conditions" } } },
                    },
                    plugins: { trigger: new FormValidation.plugins.Trigger({ event: { password: !1 } }), bootstrap: new FormValidation.plugins.Bootstrap5({ rowSelector: ".fv-row", eleInvalidClass: "", eleValidClass: "" }) },
                })),

                t.addEventListener("click", function (s) {
                    s.preventDefault(),
                    a.revalidateField("password"),
                
                    a.validate().then(function (a) {
                        "Valid" == a
                            ? (t.setAttribute("data-kt-indicator", "on"),
                                (t.disabled = !0),
                
                                setTimeout(function () {
                
                                    t.removeAttribute("data-kt-indicator"),
                
                                        (t.disabled = !1),
                
                                        // send an AJAX request
                                        $.ajax({
                                            type: "POST",
                                            url: "http://127.0.0.1:3000/auth/sign-up/",
                                            data: $('#kt_sign_up_form').serialize(),
                                            success: function(data) {
                                                console.log(data);
                                                if (data.status == 200){
                                                    Swal.fire({ 
                                                        text: data.message, 
                                                        icon: "success", 
                                                        buttonsStyling: false, 
                                                        confirmButtonText: "Ok, got it!", 
                                                        customClass: { confirmButton: "btn btn-primary" } 
                                                    }).then(function (t) {
                                                        if (t.isConfirmed) {
                                                            // redirect to the login page
                                                            window.location.href = data.redirect;
                                                         }
                                                    });
                                                    // Show success message
                                                }else if (data.status == 400){
                                                    // Show email error message
                                                    $('#email-error').text(data.message);
                                                    $('#email-error').show();
                                                }else if (data.status == 401){
                                                     $('#password-error').text(data.message);
                                                     $('#password-error').show();
                                                }else if (data.status == 402){
                                                    $('#phone_number-error').text(data.message);
                                                    $('#phone_number-error').show();
                                                }
                                    
                                                },
                                              
                                            error: function(jqXHR, textStatus, errorThrown) {
                                                console.log("Exiting SWAL", errorThrown);
                                                Swal.fire({
                                                    text: "Sorry, an error occurred while submitting the form. Please try again.",
                                                    icon: "error",
                                                    buttonsStyling: false,
                                                    confirmButtonText: "Ok, got it!",
                                                    customClass: { confirmButton: "btn btn-primary" },
                                                });
                                            },
                                        },500);

                                        
                
                                        // end added manually
                
                                }, 1500))
                
                            : Swal.fire({
                                    text: "Sorry, looks like there are some errors detected, please try again.",
                                    icon: "error",
                                    buttonsStyling: !1,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: { confirmButton: "btn btn-primary" },
                                });
                    });
                });
                e.querySelector('input[name="password"]').addEventListener("input", function () {
                    this.value.length > 0 && a.updateFieldStatus("password", "NotValidated");
                });
        },
    };
})();
KTUtil.onDOMContentLoaded(function () {
    KTSignupGeneral.init();
});
