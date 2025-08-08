const btn1 = document.getElementById('btn1');
const btn2 = document.getElementById('btn2');
const btn3 = document.getElementById('btn3');
const home = document.getElementById('home');
const work = document.getElementById('work');
const other = document.getElementById('other');


btn1.addEventListener("click", ()=> {
    home.classList.add('bg-[#F44336]', 'text-white');
    work.classList.remove('bg-[#F44336]', 'text-white');
    other.classList.remove('bg-[#F44336]', 'text-white');
})


btn2.addEventListener("click", ()=> {
    home.classList.remove('bg-[#F44336]', 'text-white');
    work.classList.add('bg-[#F44336]', 'text-white');
    other.classList.remove('bg-[#F44336]', 'text-white');
})


btn3.addEventListener("click", ()=> {
    home.classList.remove('bg-[#F44336]', 'text-white');
    work.classList.remove('bg-[#F44336]', 'text-white');
    other.classList.add('bg-[#F44336]', 'text-white');
})

