$(document).ready(function() {

  $('.date-picker').each(function() {
  	$(this).datepicker({
  		dateFormat: 'yy-mm-dd',
  		yearRange: "2017:2018",
  		todayHighlight: true,
  	});
  });

  $('#time-picker').timepicker({
	    timeFormat: 'H:i',
	    minTime: '9:00',
	    maxTime: '18:00'
  });
});
	