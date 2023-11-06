$(document).ready(function () {
    $('.paywithrazorpay').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phonenumber = $("[name='phonenumber']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(fname == "" || lname ==""|| email ==""|| phonenumber ==""|| address ==""|| city ==""|| state ==""|| country ==""|| pincode =="")
        {
            
            Swal.fire(
                'alert!',
                'all fields are mandatory!',
                'error'
              )
            return false;
        }
        else
        {   
            $.ajax({
                type: "GET",
                url: "/proceed-to-pay",
               
                success: function (response) {
                    console.log(response);

                    var options = {
                        "key": "rzp_test_ezNFJKD1s3YiJa", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_Price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "electron", //your business name
                        "description": "thank you",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/",
                        "handler": function(responseb){
                            alert(responseb.razorpay_payment_id)

                            data = {
                                 "fname":fname,
                                 "lname":lname,
                                 "email":email,
                                 "phonenumber":phonenumber,
                                 "address":address,
                                 "city":city,
                                 "state":state,
                                 "country":country,
                                 "pincode":pincode,
                                 "payment_mode":"paid by razorpay",
                                 "payment_id":responseb.razorpay_payment_id,
                                 csrfmiddlewaretoken:token


                            }

                            $.ajax({
                                type: "POST",
                                url: "/placeorder",
                                data: data,
                                
                                success: function (responsec) {

                                    Swal.fire(
                                        'congratulations!',
                                        responsec.status,
                                        'success'
                                      ).then((value) => {
                                        window.location.href ="/myorders"
                                      });
                                      Swal(responsec.status)

                                    
                                }
                            });



                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
                            "name": fname+" "+lname, //your customer's name
                            "email": email,
                            "contact": phonenumber //Provide the customer's phone number for better conversion rates 
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    
                    rzp1.open();
                    
                    
                }
            });

            
    

        }
        
        
        
        
    });
});