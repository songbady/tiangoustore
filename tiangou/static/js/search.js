$(function(){

	var error_search = false;
	

	$('#search').blur(function() {
		check_search();
	});

	

	function check_search(){
		

		if($('#search').val()=='')
		{
			
			error_search = true;
		}
		else
		{
			error_search = false;
		}
	}



	$('form').submit(function() {
		
		check_search();

		if(error_search == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








})