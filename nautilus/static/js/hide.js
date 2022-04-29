let count = 0;
let checkboxes = document.querySelectorAll(".acb"); //node list
let parent = document.querySelectorAll(".parent"); //node list
// change to array 
let checkboxArray = Array.from(checkboxes); //array
let parentArray = Array.from(parent); //array

let heading = document.querySelector("#hide"); //heading element


for (let i = 0; i < checkboxArray.length; i++) {
  parentArray[i].addEventListener("click", () => {
    if (checkboxArray[i].checked === false) {
      checkboxArray[i].checked === true;
      count++;
      console.log(count)

    }else {
        checkboxArray[i].checked === false;
        if (count !== 0) {
      count--;
    }
    }
    if (count == 2) {
      heading.classList.add("show");
    } else {
      heading.classList.remove("show");
    }
  });
}




