const button = document.getElementById('notification_button')
const toasts = document.getElementById('toasts')
const bell  = document.getElementById('notification')

const messages = [
    'Message One',
    'Message Two',
    'Message Three',
    'Message Four',
]

const types = ['info', 'success', 'warning']

button.addEventListener('click', () => createNotification())

function createNotification(message = null, type = null) {
    const notify = document.createElement('div')
    const count = Number(bell.getAttribute('data-count')) || 0;

    bell.setAttribute('data-count', count + 1);
    bell.classList.add('show-count');
    bell.classList.add('notify');

    notify.classList.add('toast')
    notify.classList.add(type ? type : getRandomType())

    notify.innerText = message ? message : getRandomMessage()

    toasts.appendChild(notify)

    setTimeout(() => {
        notify.remove()
        /*count.remove()*/
    }, 3000)

}

    bell.addEventListener("animationend", function(event) {
    bell.classList.remove('notify');
    bell.classList.remove('count');

});

function getRandomMessage() {
    return messages [ Math.floor(Math.random() * messages.length)
    ]
}

function getRandomType() {
    return types [ Math.floor(Math.random() * types.length)
    ]
}