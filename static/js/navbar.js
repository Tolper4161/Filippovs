let is_activated = false

document.getElementById("menu-bar").onclick = function()
{
    if (!is_activated)
    {
        document.getElementById("header-nav").style = "display: block;"
    }
    else
    {
        document.getElementById("header-nav").style = "display: none;"
    }
    is_activated = !is_activated
}