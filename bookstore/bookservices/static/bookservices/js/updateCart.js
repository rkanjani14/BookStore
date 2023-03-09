$(".update-cart-home").click(function(){
    var bookId = $(this).data("book")
    var action = $(this).data("action")
    updateCart(bookId,cartNumber=null,action)
})

$(".update-cart").on('change',function(){
    var bookId = $(this).data("book")
    var cartNumber = $(this).val()
    updateCart(bookId,cartNumber,action=null)
})

$(".delete-cart").on('click',function(){
    var bookId = $(this).data("book")
    updateCart(bookId,0,action=null)
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function updateCart(bookId,cartNumber,action){
    data = { "bookId":bookId,"cartNumber":cartNumber,"action":action}
    $.ajax({
      type: "POST",
      url: "/update_cart/",
      headers: {'X-CSRFToken': csrftoken},
      data: JSON.stringify(data),
      dataType: 'json',
      success: function(data){
        location.reload();
      }
    });
}