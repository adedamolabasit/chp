
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
      // count++;
      if (count < 2) {
      checkboxArray[i].checked = false;   
        count++
      }
      else {
      checkboxArray[i].checked = true;    
      }
      console.log(count)
    }else {
        checkboxArray[i].checked = true;
        if (count !== 0) {
      count--;
    }
    console.log(count)
    }
    if (count === 2) {
      heading.classList.add("show");
    } else if (count >= 2)  {
      heading.classList.remove("show");
      checkboxArray[i].checked = true;
      alert ("select two responses");


    
    } else if (count === 1)  {
        heading.classList.remove("show");
       
      }
  });
}



 



