window.onclick = function(event) {
    var target = event.target ;
    if(target.matches('.clickableBtn')) {
        var clickedEle = document.activeElement.id ;
        var ele = document.getElementById(clickedEle);
        alert(ele.text);
    }
}