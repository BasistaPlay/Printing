// $(function() {

// 	'use strict';

// 	// Form

// 	var contactForm = function() {

// 		if ($('#contactForm').length > 0 ) {
// 			$( "#contactForm" ).validate( {
// 				rules: {
// 					name: "required",
// 					email: {
// 						required: true,
// 						email: true
// 					},
// 					message: {
// 						required: true,
// 						minlength: 5
// 					}
// 				},
// 				messages: {
// 					name: "Please enter your name",
// 					email: "Please enter a valid email address",
// 					message: "Please enter a message"
// 				},
// 				/* submit via ajax */
// 				submitHandler: function(form) {		
// 					var $submit = $('.submitting'),
// 						waitText = 'Submitting...';

// 					$.ajax({   	
// 				      type: "POST",
// 				      url: "php/send-email.php",
// 				      data: $(form).serialize(),

// 				      beforeSend: function() { 
// 				      	$submit.css('display', 'block').text(waitText);
// 				      },
// 				      success: function(msg) {
// 		               if (msg == 'OK') {
// 		               	$('#form-message-warning').hide();
// 				            setTimeout(function(){
// 		               		$('#contactForm').fadeOut();
// 		               	}, 1000);
// 				            setTimeout(function(){
// 				               $('#form-message-success').fadeIn();   
// 		               	}, 1400);
			               
// 			            } else {
// 			               $('#form-message-warning').html(msg);
// 				            $('#form-message-warning').fadeIn();
// 				            $submit.css('display', 'none');
// 			            }
// 				      },
// 				      error: function() {
// 				      	$('#form-message-warning').html("Something went wrong. Please try again.");
// 				         $('#form-message-warning').fadeIn();
// 				         $submit.css('display', 'none');
// 				      }
// 			      });    		
// 		  		}
				
// 			} );
// 		}
// 	};
// 	contactForm();

// });

const toast = document.querySelector(".toast");
(closeIcon = document.querySelector(".close")),
  (progress = document.querySelector(".progress"));

let timer1, timer2;

  toast.classList.add("active");
  progress.classList.add("active");

  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000);

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);

closeIcon.addEventListener("click", () => {
  toast.classList.remove("active");

  setTimeout(() => {
    progress.classList.remove("active");
  }, 300);

  clearTimeout(timer1);
  clearTimeout(timer2);
});