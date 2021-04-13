
/* Vol control */

const range = document.getElementById('range')

range.addEventListener('input', (e) => {
    const value = +e.target.value
    const label = e.target.nextElementSibling

    const range_width = getComputedStyle(e.target).getPropertyValue('width')
    const label_width = getComputedStyle(label).getPropertyValue('width')

    const num_width = +range_width.substring(0, range_width.length - 2)
    const num_label_width = +label_width.substring(0, label_width.length - 2)

    const max = +e.target.max
    const min = +e.target.min

    const left = value * (num_width/max) - num_label_width / 2 + scale(value, min, max, 10, -10)

    label.style.left = `${left}px`

    label.innerHTML = value + ` `+`<i class="fas fa-volume-up"></i>`

})

// https://stackoverflow.com/questions/10756313/javascript-jquery-map-a-range-of-numbers-to-another-range-of-numbers
const scale = (num, in_min, in_max, out_min, out_max) => {
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  }


/* Vol control - old
const range = document.getElementById('range');
const rangeV = document.getElementById('rangeV');
  
setValue = ()=>{
    const newValue = Number( (range.value - range.min) * 100 / (range.max - range.min) );
    const newPosition = 10 - (newValue * 0.2);
    rangeV.innerHTML = `<span>${range.value}</span>`;
    rangeV.style.top = `calc(${newValue}% + (${newPosition}px))`;
  };
document.addEventListener("DOMContentLoaded", setValue);
range.addEventListener('input', setValue); */

/* Temp control */

const tincreaseBtn = document.getElementById('t_increase');
const tdecreaseBtn = document.getElementById('t_decrease');
const tsizeEL = document.getElementById('t_size');

let t_size = 68

function updateTempSizeOnScreen() {
    tsizeEL.innerHTML = `<i class="fas fa-thermometer-three-quarters"></i>` + t_size
}


    tincreaseBtn.addEventListener('click', () => {
        t_size += 1
    
        if(t_size > 90) {
            t_size = 90
        }
    
        updateTempSizeOnScreen()
    })


if(tdecreaseBtn) {
    tdecreaseBtn.addEventListener('click', () => {
        t_size -= 1
    
        if(t_size < 25) {
            t_size = 25
        }
    
        updateTempSizeOnScreen()
    })
}

/* Open / close button */

function lockFunction(x) {
    x.classList.toggle("fa-unlock");
  }



/* Fan */
const fincreaseBtn = document.getElementById('f_increase');
const fdecreaseBtn = document.getElementById('f_decrease');
const fsizeEL = document.getElementById('f_size');

let f_size = 1;


function updateFanSizeOnScreen() {
    fsizeEL.innerHTML = `<i class="fas fa-fan"></i>`+f_size
}


    fincreaseBtn.addEventListener('click', () => {
        f_size += 1
    
        if(f_size > 6) {
            f_size = 6
        }
    
        updateFanSizeOnScreen()
    })


    fdecreaseBtn.addEventListener('click', () => {
        f_size -= 1
    
        if(f_size < 1) {
            f_size = 1
        }
    
        updateFanSizeOnScreen()
    })


    