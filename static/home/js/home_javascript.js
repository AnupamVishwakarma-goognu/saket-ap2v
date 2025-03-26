$(document).ready(function(){
	let container = $(".testimonials-new").find(".scroll-wrapper")
	let column = container.find(".testimonials-column")
	let columnWidth = column.outerWidth(true)
	let containerScrollWidth = container[0].scrollWidth;
	let containerVeiwWidth = container[0].offsetWidth;
	let scrollLength = containerScrollWidth - containerVeiwWidth;
	let scrollLocation = 0;
	setInterval(function(){
		scrollLocation += columnWidth;
		if (scrollLocation > scrollLength ){
			scrollLocation=0;
		}
		container.animate({ scrollLeft: scrollLocation },1000);
	},5000)
})