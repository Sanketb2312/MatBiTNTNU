function dropdown_allergies() {
    document.getElementById("dropdownAllergies").classList.toggle("show");
}

function dropdown_locations() {
    document.getElementById("dropdownLocations").classList.toggle("show");
}


function filter() {
    var checkedValueAllergy = document.querySelectorAll('.allergyCheck:checked');
    var checkedValueLocation = document.querySelectorAll('.locationCheck:checked');

    notInclude = [];
    for (var key in events_allergy) {
        for(var i = 0; i < checkedValueAllergy.length; i++){
            if (events_allergy[key].includes(parseInt(checkedValueAllergy[i].value))) {
                notInclude.push(parseInt(key))
            }
        }
    }

    if (checkedValueLocation.length !== 0) {
        for (var key in events_location) {
            var includeBool = false
            for(var i = 0; i < checkedValueLocation.length; i++){
                if (events_location[key].includes(checkedValueLocation[i].value)) {
                  includeBool = true
                }
            }
            if (!includeBool) notInclude.push(parseInt(key))
        }
    }

    for (var i = 0; i < allEvents.length; i++) {
        key = allEvents[i]
        var dinner = document.getElementById("allergy-"+key)
        if (notInclude.includes(key)) {
            dinner.style.display ="none";
        } else {
            dinner.style.display ="initial";
        }
    }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
