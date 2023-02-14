let count     = 0
function checkCredentials() {
    var email = document.querySelector(".email").value;
    var password = document.querySelector("input[name='password']").value;

    // package data in a JSON object
    var data_d = {'email':  email, 'password': password}
    console.log('data_d', data_d)

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(returned_data){
            returned_data = JSON.parse(returned_data);
            
              if (returned_data['success'] == 1){
                count = 0;
                document.querySelector(".count").innerHTML = count;
                document.querySelector(".fail-msg").style.display = "none";
                window.location.href = "/home";

            }else{
                count += 1;
                document.querySelector(".count").innerHTML = count;
                var failMsg = document.querySelectorAll(".fail-msg");
                for(var i = 0; i < failMsg.length; i+=1){
                    failMsg[i].style.opacity = "1";
                }
            }
            }
        

    
    });
}