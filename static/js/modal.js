document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('#add-product')
    const panel = document.querySelector('#admin-adding-panel')
    const closeBtn = document.querySelector('#admin-adding-panel-close-btn')
    if (button != null && closeBtn != null)
    {
        button.addEventListener('click', () => {
            panel.classList = 'active'
        })
        closeBtn.addEventListener('click', () => {
            panel.classList = 'unactive'
        })
    }
})