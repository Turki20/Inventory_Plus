

function remove_parent(el) {
    el.parentElement.remove()
}


state = false
menu_list = document.querySelector('#left_side')
function open_menu() {
    if (state) {
        menu_list.style.left = '-25%'
        menu_list.style.position = 'absolute';
        state = !state
    }else{
        menu_list.style.left = '0'
        menu_list.style.position = 'relative';
        state = !state
    }

}