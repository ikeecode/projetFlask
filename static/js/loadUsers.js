var myform = document.querySelector('#changementUser')
var submitBtn = document.querySelector('button#submitBtn');

submitBtn.addEventListener('click', (e)=>{
  e.preventDefault()
  myform.submit()
})


var inputField = document.querySelector('#numberChosen');
inputField.placeholder = 'inserer le nombre à charger';
