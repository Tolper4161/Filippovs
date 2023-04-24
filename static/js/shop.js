let is_visible = false

// name, picture, price, discription, tags
function showProduct(id)
{
    console.log(id)
    if (!is_visible) {
        document.getElementById(id).classList.remove("unactive")
        document.getElementById(id).classList.toggle("active")
    }
    else {
        document.getElementById(id).classList.toggle("unactive")
        document.getElementById(id).classList.remove("active")
    }
    is_visible = !is_visible
}