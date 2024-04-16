const allLikeForms = document.querySelectorAll('#messages-form')

for (let form of allLikeForms) {
    form.addEventListener('click', handleClick)
}

async function handleClick(evt) {
    evt.preventDefault()
    const likeBtn = this.firstElementChild
    const msg_id = likeBtn.dataset.warble_id
    const response = await axios.post(`/users/add_remove_like/${msg_id}`)
    const data = response.data
    if (data.liked) {
        likeBtn.classList.remove('btn-secondary')
        likeBtn.classList.add('btn-primary')
    } else {
        likeBtn.classList.remove('btn-primary')
        likeBtn.classList.add('btn-secondary')
    }
}