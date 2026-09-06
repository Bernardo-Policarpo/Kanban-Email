function open_modal(nome) {
    const modal = document.getElementById(`${nome}_modal`);
    modal.showModal();
}

function close_modal(nome) {
    const modal = document.getElementById(`${nome}_modal`);
    modal.close();
}

const selectedCardsKey = "selectedKanbanCards";
function getSelectedCards() {
    const cards = localStorage.getItem(selectedCardsKey);
    if (!cards) {
        return [];
    }
    return JSON.parse(cards);
}
function saveSelectedCards(cards) {
    const uniqueCards = [...new Set(cards)];
    localStorage.setItem(
        selectedCardsKey,
        JSON.stringify(uniqueCards)
    );
}
function updateSelectedCards() {
    const selectedCards = getSelectedCards();
    document.querySelectorAll('input[name="cartoes"]').forEach(function(input) {
        const cardValue = input.value;
        if (input.checked && !selectedCards.includes(cardValue)) {
            selectedCards.push(cardValue);
        }
        if (!input.checked) {
            const index = selectedCards.indexOf(cardValue);
            if (index !== -1) {
                selectedCards.splice(index, 1);
            }
        }
    });
    saveSelectedCards(selectedCards);
}
function restoreSelectedCards() {
    const selectedCards = getSelectedCards();
    document.querySelectorAll('input[name="cartoes"]').forEach(function(input) {
        input.checked = selectedCards.includes(input.value);
    });
}
document.addEventListener("DOMContentLoaded", function() {
    restoreSelectedCards();
    document.querySelectorAll('input[name="cartoes"]').forEach(function(input) {
        input.addEventListener("change", function() {
            updateSelectedCards();
        });
    });
    const searchForm = document.getElementById("searchCodeForm");
    if (searchForm) {
        searchForm.addEventListener("submit", function() {
            updateSelectedCards();
        });
    }
    const sendEmailForm = document.getElementById("sendEmailForm");
    if (sendEmailForm) {
        sendEmailForm.addEventListener("submit", function(event) {
            updateSelectedCards();
            const selectedCards = getSelectedCards();
            if (selectedCards.length === 0) {
                event.preventDefault();
                alert("Selecione pelo menos um cartão.");
                return;
            }
            document
                .querySelectorAll('input[name="cartoes"]')
                .forEach(function(input) {
                    input.removeAttribute("name");
                });
            selectedCards.forEach(function(card) {
                const hiddenInput = document.createElement("input");
                hiddenInput.type = "hidden";
                hiddenInput.name = "cartoes";
                hiddenInput.value = card;
                sendEmailForm.appendChild(hiddenInput);
            });
        });
    }
    const confirmSendEmailForm = document.getElementById("confirmSendEmailForm");
    if (confirmSendEmailForm) {
        confirmSendEmailForm.addEventListener("submit", function() {
            localStorage.removeItem(selectedCardsKey);
        });
    }
});
