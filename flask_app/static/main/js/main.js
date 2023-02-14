// Toggles visibility of the main feedback box once the button is pressed
// Citation: https://codepen.io/draw/pen/GWzWgr
function toggle_visibility() {
    var e = document.getElementById('feedback-main');
    if(e.style.display === 'block')
       e.style.display = 'none';
    else
       e.style.display = 'block';
 }


function toggle_res_visibility() {
   var e = document.getElementById('newres-main');
   if(e.style.display === 'block')
      e.style.display = 'none';
   else
      e.style.display = 'block';
}

function toggle_edit_visibility() {
   var e = document.getElementById('edit-main');
   if(e.style.display === 'block')
      e.style.display = 'none';
   else
      e.style.display = 'block';
}

