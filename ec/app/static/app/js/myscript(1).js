$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Assuming this is the quantity element
    console.log("pid=", id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data = ", data);
            // Update the quantity in the specific element
            $(eml).text(data.quantity); // Use jQuery to update the text
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});


$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]; // Assuming this is the quantity element
    console.log("pid=", id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data = ", data);
            // Update the quantity in the specific element
            $(eml).text(data.quantity); // Use jQuery to update the text
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});


$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Get the product ID
    var cartItem = $(this).closest('.row'); // Get the closest row (cart item)
    
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: { prod_id: id },
        success: function(data) {
            // Update displayed amounts
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
            // Remove the cart item from the DOM
            cartItem.remove();
            // Check if the cart is empty after removal
            if ($('.row').length === 0) {
                $('.container').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: ", status, error);
        }
    });
});





$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})