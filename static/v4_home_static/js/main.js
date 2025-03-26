

$('.home-slider').slick({
  dots: true,
  arrows: true,

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
        slidesToScroll: 2,
        dots: true,
        arrows:false,
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        dots: true,
        arrows:false,
      }
    }
  ]
});

$('.testimonials__slider').slick({
  dots: true,
  arrows: false
});

$('.product-slider').slick({
  slidesToShow: 4,
  slideWidth:275,
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

$('.slide_3').slick({
  slidesToShow: 3,
  slideWidth:350,
  slidesToScroll: 1,
  dots:true,
  arrows:false,

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

$('.certification--slider').slick({
  slidesToShow: 2,
  slideWidth:300,
  slidesToScroll: 1,
  dots: true,
  arrows: false,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 1,
        infinite: true,
        dots: true,
      arrows: false,
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,

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

$('.slide_2').slick({
  slidesToShow: 2,
  slideWidth:300,
  slidesToScroll: 1,
  dots: true,

  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 1,
        infinite: true,
        dots: true,
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,

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

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
  $('.product-slider').slick('setPosition');
})


$(function() {
  $(".dropdown").hover(
      function(){ $(this).addClass('show') },
      function(){ $(this).removeClass('show') },
  );

});


$('.courses-tabs > .nav-tabs > li ').hover(function() {
  if ($(this).hasClass('hoverblock'))
    return;
  else
    $(this).find('a').tab('show');
});



$(document).ready(function() {
  $('.dropdown').hover(function(){
      $('.overlay').addClass('show');
  },
  function(){
      $('.overlay').removeClass('show');
  });

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
    $(".forget-password").addClass('hide');


  });  $("#sign-up1").click(function(){
    $("#right-panel").addClass("move-left");
    $(".login-modal__left-pan").addClass("move-right-disappear");
    $(".forget-password").addClass('hide');


  });

  $("#sign-in").click(function(){
    $("#right-panel").removeClass("move-left");
    $(".login-modal__left-pan").removeClass("move-right-disappear");
  });

});// end of document


// Full page Search
$(document).ready(function() {

  $(".search-panel__input input").focus(function() {
  $('.suggestor').show('fast');
  $('.recent-search').hide();
  //return false;
});

  $('.search-panel__input input').blur(function(){
    if( !$(this).val() ) {
        $('.suggestor').hide('fast');
        $('.recent-search').show();
    }
  });

  $('.recent-search__heading--link').click(function(){
    $('.recent-search').hide();
  });

  $('.cls_search-btn').click(function(){
    $('.full-page-search').show();
    $('body').addClass('body-fixed');
  });

  $('#close-search').click(function(){
    $('.full-page-search').hide();
    $('body').removeClass('body-fixed');
  });

});// end of document


$('#close-banner').click(function(event){
  event.preventDefault();

});

/* Disable push-banner
$('.main-wrap').addClass('pushed');
*/

$('#close-banner').click(function(event){
  event.preventDefault();
  $('.main-wrap').removeClass('pushed');
});


// Jquery for expand and collapse the sidebar
$('#bar-menu').click(function(){
  $('.sidebar').addClass('side-menuX');
  $('.menu-overlay').addClass('hmenu-opaque');
  $('body').addClass('body-fixed');
});

$('#close-sidebar, .menu-overlay').click(function(){
  $('.sidebar').removeClass('side-menuX');
  $('.menu-overlay').removeClass('hmenu-opaque');
  $('body').removeClass('body-fixed');
});



$('.cls_login').click(function(){
  $('#mobile-login').addClass('slideXright');
  $('.menu-overlay').removeClass('hmenu-opaque');
  $('.sidebar').removeClass('side-menuX');
  $('body').addClass('body-fixed');
});

$('.btn-back').click(function(){
  $('#mobile-login').removeClass('slideXright');
  $('body').removeClass('body-fixed');
});

$('.btn-back2').click(function(){
  $('#mobile-login').removeClass('slideXright');
  $('body').removeClass('body-fixed');
});

$('.cls_register').click(function(){
  $('#mobile-registration').addClass('slideXright');
  $('.menu-overlay').removeClass('hmenu-opaque');
  $('.sidebar').removeClass('side-menuX');
  $('body').addClass('body-fixed');
});

$('.btn-back').click(function(){
  $('#mobile-registration').removeClass('slideXright');
  $('body').removeClass('body-fixed');
});

$('.btn-back2').click(function(){
  $('#mobile-registration').removeClass('slideXright');
  $('body').removeClass('body-fixed');
});

$('#mobile-signin').click(function(){
  $('#mobile-registration').removeClass('slideXright');
  $('#mobile-login').addClass('slideXright');
  $('body').addClass('body-fixed');
});

$('#mobile-signup').click(function(){
  $('#mobile-registration').addClass('slideXright');
  $('#mobile-login').removeClass('slideXright');
  $('body').addClass('body-fixed');
});





// $('.sidebar__category--item a').click(function (event) {
//   $('.sidebar__category').addClass('slide-left');
// });


// $('.sub-headingwrap').click(function (event) {
//   $('.sidebar__sub-category').removeClass('slide-left');
// });



// // Search By Category
// $('.sidebar__category--item a').click(function (e) {
//   e.preventDefault();
//   var $this = $(this);
//   if ($this.hasClass('slide-left')) {
//     $this.removeClass('slide-left');
//   } else {
//     $this.next('.sidebar__sub-category').removeClass('slide-left');
//     $this.next('.sidebar__sub-category').addClass('slide-left');
//   }
// });

// Search By Category
$('.sidebar__category--item a').click(function (e) {
  e.preventDefault();
  var slug_name = $(this).data("target");

  $('.sidebar__category').addClass('slide-left');
  $('#sub-'+slug_name).addClass('slide-left');
});

$('.back-btn').click(function (event) {
  $('.sidebar__category').removeClass('slide-left');
  $('.sidebar__sub-category').removeClass('slide-left');
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


// $(document).ready(function () {
//   $(".show_hide").on("click", function () {
//       var txt = $("#test").is(':visible') ? 'Read More' : 'Read Less';
//       $(".show_hide").text(txt);
//       $(this).prev('#test').slideToggle(200);
//   });
// });

// Scroll Top sticky footer
// var stickyfooter = $('#bottomScroll');
// $(window).scroll(function() {
//   if ($(window).scrollTop() > 10) {
//     stickyfooter.addClass('bottom-visible');
//   } else {
//     stickyfooter.removeClass('bottom-visible');
//   }
// });

$(document).ready(function(){
  //disappear nav when a attribute is clicked
	$('nav ul li a').click( function() {
		$('nav ul').toggleClass("showing");
	});

});

// On scroll fixed header,m
$(window).scroll(function(){
  var heightPushDown = $('.push-down-banner').outerHeight();
  // var heightBanner = $('.banner-inner').outerHeight();

  var allHeight= (heightPushDown);
  if ($(window).scrollTop() >= allHeight) {
      $('#main-navigation').addClass('fixed-header');
      $('.main-wrap').css('padding-top', '67px');
  }
  else {
      $('#main-navigation').removeClass('fixed-header');
      $('.main-wrap').css('padding-top', '0');
  }
});

// On scroll fixed main Navigation
$(window).scroll(function(){
  var heightPushDown = $('.push-down-banner').outerHeight();
  var heightNavBar = $('.navbar').outerHeight();
  var heightBanner = $('.banner-inner').outerHeight();

  var allHeight= (heightPushDown + heightNavBar + heightBanner);
  if ($(window).scrollTop() >= allHeight) {
      $('.secondary-menu').addClass('secondary-menu-fixed');
      $('.main-wrap').addClass('secondary-menu-wrap');
  }
  else {
      $('.secondary-menu').removeClass('secondary-menu-fixed');
      $('.main-wrap').removeClass('secondary-menu-wrap');
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


function slide(direction){
  var container = document.getElementById('coursesTab');
  scrollCompleted = 0;
  var slideVar = setInterval(function(){
      if(direction == 'left'){
          container.scrollLeft -= 10;
      } else {
          container.scrollLeft += 10;
      }
      scrollCompleted += 10;
      if(scrollCompleted >= 100){
          window.clearInterval(slideVar);
      }
  }, 50);
}


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

  $(function(){
    var gallery = $('.gallery a').simpleLightbox();
});
//Photo Gallery Function 

  
  $(function() {
    $('.acc__title').click(function(j) {
      
      var dropDown = $(this).closest('.acc__card').find('.acc__panel');
      $(this).closest('.acc').find('.acc__panel').not(dropDown).slideUp();
      
      if ($(this).hasClass('active')) {
        $(this).removeClass('active');
      } else {
        $(this).closest('.acc').find('.acc__title.active').removeClass('active');
        $(this).addClass('active');
      }
      
      dropDown.stop(false, true).slideToggle();
      j.preventDefault();
    });
  });

