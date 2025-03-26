$('.slide_3').slick({
  slidesToShow: 3,
  slideWidth:350,
  slidesToScroll: 1,
  dots:false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});


$('.product-slider').slick({
  slidesToShow: 3,
  slideWidth:370,
  slidesToScroll: 1,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});

$('.prog-tools').slick({
  slidesToShow: 6,
  slideWidth:370,
  slidesToScroll: 1,
  control: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});

$('.faculty-slider').slick({
  slidesToShow: 4,
  slideWidth:260,
  slidesToScroll: 1,
  control: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});

$('.review-slider').slick({
  slidesToShow: 3,
  slideWidth:260,
  slidesToScroll: 1,
  control: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});

$('.learners-slider').slick({
  slidesToShow: 1,
  slideWidth:540,
  slidesToScroll: 1,
  control: false,
  dots:true,
  arrows: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});


$('.industry-projects-slider').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  control: false,
  dots:false,
  vertical: true,
  infinite: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ]
});


$('.slick', '.vertical-slider').slick({
  vertical: true,
  verticalSwiping: true,
  slidesToShow: 1,
  slidesToScroll: 1
});

    

// Scroll Top function
var btn = $('#btnScrollTop');
$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('top-visible');
  } else {
    btn.removeClass('top-visible');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});



$(document).ready(function(){
	

  //disappear nav when a attribute is clicked
	$('nav ul li a').click( function() {
		$('nav ul').toggleClass("showing");
	});
  
});

// On scroll fixed header,m 
$(window).scroll(function(){
  var heightNavBar = $('.navbar').outerHeight();
  var heightBanner = $('.banner-inner').outerHeight();

  var allHeight= (heightNavBar + heightBanner);
  if ($(window).scrollTop() >= allHeight) {
      $('#mainNav').addClass('fixed-header');
  }
  else {
      $('#mainNav').removeClass('fixed-header');
  }
});


// On scroll fixed Side on listing page
$(window).scroll(function(){
  var heightPushDown = $('.push-down-banner').outerHeight();
  var heightNavBar = $('.navbar').outerHeight();
  var heightBanner = $('.banner-inner').outerHeight();
  var heightAppliedFilter = $('.applied-filter').outerHeight() + 50;

  var allHeight= (heightPushDown + heightNavBar + heightBanner + heightAppliedFilter);
  
  if ($(window).scrollTop() >= allHeight) {
      $('#sidebar').addClass('fixed-side');
  }
  else {
      $('#sidebar').removeClass('fixed-side');
  }
});


  // Select all links with hashes
  // $('a[href*="#"]')
  $('a.page-scroll')
  // Remove links that don't actually link to anything
  .click(function(event) {
      // Figure out element to scroll to
  
      var target = $(this.hash);
      var heightNavbar = $('.navbar').outerHeight();
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();

        $('.secondary-menu a').each(function () {
          $(this).removeClass('active');
        })
        $(this).addClass('active');
  
        $('html, body').animate({
          scrollTop: target.offset().top -heightNavbar
        }, 800, function() {
          
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
  });


  

$(document).ready(function() {

  $(".animation-input").val(""); 
  $(".animation-input").focusout(function(){ 
    if($(this).val() != ""){ 
      $(this).parent().parent().addClass("has-content"); 
    }else{ 
      $(this).parent().removeClass("has-content"); } 
  }) 


  $("#sign-up").click(function(){
    $("#right-panel").addClass("move-left");
    $(".login-modal__left-pan").addClass("move-right-disappear");
  

  });  $("#sign-up1").click(function(){
    $("#right-panel").addClass("move-left");
    $(".login-modal__left-pan").addClass("move-right-disappear");
  

  });
  
  $("#sign-in").click(function(){
    $("#right-panel").removeClass("move-left");
    $(".login-modal__left-pan").removeClass("move-right-disappear");
  });

});// end of document 