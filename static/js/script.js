```javascript
// ===============================
// Navbar Shadow On Scroll
// ===============================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 50) {
        navbar.classList.add("shadow");
    } 
    else {
        navbar.classList.remove("shadow");
    }

});




// ===============================
// Dark Mode Toggle
// ===============================

const themeButton = document.getElementById("themeToggle");


if(themeButton){

    themeButton.addEventListener("click", function(){

        document.body.classList.toggle("dark-mode");


        if(document.body.classList.contains("dark-mode")){

            themeButton.innerHTML = "☀️";

        }
        else{

            themeButton.innerHTML = "🌙";

        }


    });

}




// ===============================
// Search Box Animation
// ===============================

const searchBox = document.querySelector(".search-box");


if(searchBox){


    searchBox.addEventListener("focus", function(){

        searchBox.style.width = "300px";

    });



    searchBox.addEventListener("blur", function(){

        searchBox.style.width = "220px";

    });


}




// ===============================
// Smooth Scroll
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(link => {


    link.addEventListener("click", function(e){

        e.preventDefault();


        document.querySelector(this.getAttribute("href"))
        .scrollIntoView({

            behavior:"smooth"

        });


    });


});




// ===============================
// Blog Card Animation
// ===============================

const cards = document.querySelectorAll(".blog-card");


cards.forEach(card=>{


    card.addEventListener("mouseenter",()=>{

        card.style.transform="translateY(-8px)";

    });



    card.addEventListener("mouseleave",()=>{

        card.style.transform="translateY(0)";

    });



});
```
