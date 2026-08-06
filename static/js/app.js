function open_modal(nome) {
    const modal = document.getElementById(`${nome}_modal`);
    modal.showModal();
}

function close_modal(nome) {
    const modal = document.getElementById(`${nome}_modal`);
    modal.close();
}