window.onload = function () {
  let currentUrl = "";

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    currentUrl = tabs[0].url;
    console.log(currentUrl);

    const apiUrl = "http://localhost:8000/api/results";

    const dataToSend = {
      video_url: currentUrl,
    };

    var resultData = "";

    if (currentUrl != "" || currentUrl != undefined || currentUrl != null) {
      console.log("fetched");
      fetch(apiUrl + `?video_url=${dataToSend.video_url}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
      })
        .then((response) => response.json())
        .then((data) => {
          d = JSON.parse(data.data);
          console.log("Response from FastAPI:", d);
          resultData = d;

          console.log(resultData);

          document.querySelector("#po-cent").innerHTML = Math.floor(
            resultData.percentages[1]
          );
          document.querySelector("#nu-cent").innerHTML = Math.floor(
            resultData.percentages[2]
          );
          document.querySelector("#ne-cent").innerHTML = Math.floor(
            resultData.percentages[0] // Corrected index
          );

          let imp_keywds = document.querySelector("#imp-ks"); // Corrected selector

          resultData.important_keywords.forEach((e) => {
            if(e[1] == "positive") {
            var myElement = document.createElement("div");
            
            // Add classes to the div element
            myElement.classList.add(
              "rounded-lg",
              "bg-green",
              "text-p-10",
              "text-sm",
              "w-fit",
              "font-semibold",
              "text-white"
              );
              
              // Add content to the div element
              myElement.textContent = e[0];
              
              // imp_keywds.appendChild(document.createTextNode(e));
              imp_keywds.appendChild(myElement);
            }else {
              var myElement = document.createElement("div");
              
              // Add classes to the div element
              myElement.classList.add(
                "rounded-lg",
                "bg-red",
                "text-p-10",
                "text-sm",
                "w-fit",
                "font-semibold",
                "text-white"
                );
                
                // Add content to the div element
                myElement.textContent = e[0];
                
                // imp_keywds.appendChild(document.createTextNode(e));
                imp_keywds.appendChild(myElement);
              }
          });
        })
        .catch((error) => console.error("Error:", error));
    }
  });
};
