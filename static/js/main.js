/*JavaScript :: 
在input text 按下 enter 即可送出，
並且選取 text
*/
$("#todo").keydown(function(event) {
    if(event.keyCode == 13){
        checkOut();
    };
    
});