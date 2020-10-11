console.log("Start of script");


// get weather condtion
async function getConfig() {
    const url = `${window.origin}/config`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    return data;
  };

async function createConfiguration(){
  const config = await getConfig()
 

  Object.keys(config).forEach(key=>{
    console.log(key, config[key]);
    addParameter(key,config[key]);
  });
};

const configForm = document.querySelector("#configForm");
const inputs = configForm.querySelector(".input");

function addParameter(name, value){
  let label = document.createElement("label");
  label.textContent=name;
  let input = document.createElement("input");
  input.value =value;
  inputs.appendChild(label);
  inputs.appendChild(input);
  inputs.appendChild(document.createElement("br"));
  inputs.appendChild(document.createElement("br"));
}

createConfiguration()


