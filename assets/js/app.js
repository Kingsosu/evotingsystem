document.onreadystatechange = function () {
    var state = document.readyState;
    if (state == 'loading') {
        document.getElementById('preloader-spin').classList.add('show');
    } else if (state == 'complete') {
        setTimeout(function () {
            document.getElementById('preloader-spin').classList.remove('show');
        }, 100);
    }
}

let alertCommonMessage = document.querySelectorAll('.alert-common-message')

alertCommonMessage.forEach( message =>{
  setTimeout(function(){
    if(message){
        message.style.display = 'none'
    }
  }, 5000)
});