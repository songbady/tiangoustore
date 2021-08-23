$(function(){

	var error_phone = false;
	var error_email = false;


	$('#email').blur(function() {
		check_email();
	});

	$('#phone').blur(function() {
		check_phone();
	})

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_email = true;
		}
	}

	function check_phone(){
		var re = /^1[3|4|5|8][0-9]\d{4,8}$/;

		if(re.test($('#phone').val())){
			$('#phone').next().hide();
			error_phone = false;
		}
		else{
			$('#phone').next().html('手机号格式不正确')
			$('#phone').next().show();
			error_phone = true;
		}
	}


	$('.info_con').submit(function() {
		check_phone();
		check_email();

		if(error_phone == false && error_email == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








})