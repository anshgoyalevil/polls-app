var count=1;
function add_more_choice(){
    count+=1
    html='<div>\
    <label>Create Choice</label>\
    <input type="text" name="poll_choice'+count+'" placeholder="enter a choice">\
    </div>'

    var choice=document.getElementById('choice_field')
    choice.insertAdjacentHTML( 'beforeend', html)
}