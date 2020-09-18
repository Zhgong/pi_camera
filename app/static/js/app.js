console.log("Start of script");
// import { MyController } from "./control";

const btnStartRecording = document.querySelector("#startRecording");
const doms = {btnStartRecording};
const camera = new Camera()
// const controller = new MyController(doms, camera);
const controller = new MyController(doms);