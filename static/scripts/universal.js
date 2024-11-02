function getCookie(name) {

    var cookieArray = document.cookie.split(";");
  
    for (var i = 0; i < cookieArray.length; i++) {
  
      var cookiePair = cookieArray[i].split("=");
  
      if (cookiePair[0].trim() === name) {
  
        return decodeURIComponent(cookiePair[1]);
  
      }
  
    }
  
    return null;  
}

function setCookie(name, value, days) {

    var expires = "";

    if (days) {

      var date = new Date();

      date.setTime(date.getTime() + (days*24*60*60*1000));

      expires = "; expires=" + date.toUTCString();

    }

    document.cookie = name + "=" + value + expires + "; path=/";
}