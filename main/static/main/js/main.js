$(document).ready(function($) {
    "use strict";
    
    $('#container').pinto({
        itemWidth:230,
        gapX:10,
        gapY:10,
        onItemLayout: function($item, column, position) {
        }
    });
    
    $("#pintoInit").click(function(){
        $('#container').pinto();
    });
    
    $("#pintoDestroy").click(function(){
        $('#container').pinto("destroy");
    });
    
    $("#categories-dropdown").click(function(){
        if ($(".categories-hidden").css("display") == 'none'){
            $(".categories-hidden").slideDown();
        } else {
            $(".categories-hidden").slideUp();
        }
    })
    
    $(".acceptButton").click(function() {
        let offerId = this.dataset.offer;
        let winner = this.dataset.winner;
        changeStatus(offerId, {winner: winner, status: 'accepted'})
    })
    
    $(".cancelButton").click(function() { 
        let offerId = this.dataset.offer;
        changeStatus(offerId, {status: 'canceled'})
    }) 


});

function changeStatus(offerId, data) {
    fetch(`/api/offers/status/${offerId}`, {
        method: "PUT",
        redirect: 'follow',            
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },            
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status == 'ok'){
            console.log(result.status)
            location.reload();
        } else {
            console.log(result.error)
        }
        
    })     

}


// Get csrf for PUT method
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

