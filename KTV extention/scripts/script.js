


const apiUrl = 'http://localhost:8000/api/results';

// Replace this URL with the actual URL where your FastAPI server is hosted

const dataToSend = {
  video_url: "https://www.youtube.com/watch?v=9XaS93WMRQQ",
};

let resultData = "";

console.log(dataToSend.video_url);

fetch(apiUrl + `?video_url=${dataToSend.video_url}`, { // `${apiUrl}/predict
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(dataToSend),
})
  .then(response => response.json())
  .then(data => {
    let d = JSON.parse(data.data)
    console.log('Response from FastAPI:', d);
    resultData = d;

    let commentSection = document.querySelector("ytd-app");
    let content = commentSection.querySelector("#content");
    let target = content.querySelector("#masthead-container");
  //   let target1 = content.querySelector("ytd-page-manager");
  //   let target = content.querySelector("ytd-watch-flexy");
    // console.log(document);
  
    let whiteBox = document.createElement("div");
    whiteBox.style.backgroundColor = "white";
    whiteBox.style.width = "100vw";
    whiteBox.style.height = "10px";
    whiteBox.style.background = `linear-gradient(to right, #3aa159 0%, #3aa159 ${resultData.percentages[1]}%, #3aaec8 ${resultData.percentages[1]}%, #3aaec8 ${resultData.percentages[2]}%, #e1797a ${resultData.percentages[2]}%, #e1797a 100%)`;
    target.appendChild(whiteBox);
  })
  .catch(error => console.error('Error:', error));






  window.onload = function () {
    
    let commentSection = document.querySelector("ytd-app");
    let content = commentSection.querySelector("#content");
    let target = content.querySelector("#masthead-container");
  //   let target1 = content.querySelector("ytd-page-manager");
  //   let target = content.querySelector("ytd-watch-flexy");
    // console.log(document);
  
    // let whiteBox = document.createElement("div");
    // whiteBox.style.backgroundColor = "white";
    // whiteBox.style.width = "100vw";
    // whiteBox.style.height = "10px";
    // whiteBox.style.background = "linear-gradient(to right, #3aa159 0%, #3aa159 70%, #3aaec8 70%, #3aaec8 90%, #e1797a 90%, #e1797a 100%)";
    // target.appendChild(whiteBox);
  
  //   if (target) {
  //     alert("body exists");
  //   } else {
  //     alert("body does not exist");
  //   }
  
    console.log("CHECK : ", document);
    
  
  };

  // export {resultData};