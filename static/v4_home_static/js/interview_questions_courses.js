$('.owl-carousel').owlCarousel({
  items: 4,
  margin: 10,
  loop: true,
  autoplay: true,
  autoplayHoverPause: false,
  responsive: {
    0: {
      items: 1,
      nav: false,
    },
    700: {
      items: 2,
      nav: false,
    },
    1000: {
      items: 3,
      nav: false,
    },
  },
  })
